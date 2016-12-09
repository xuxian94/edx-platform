"""
Views for building plugins.
"""

from abc import abstractmethod
import logging

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.views.generic import View
from edxmako.shortcuts import render_to_string
from web_fragments.fragment import Fragment
from web_fragments.views import FragmentView, WEB_FRAGMENT_RESPONSE_TYPE

log = logging.getLogger('plugin_api')


class EdxFragmentView(FragmentView):
    """
    The base class of all Open edX fragment views.
    """
    USES_PATTERN_LIBRARY = True

    @staticmethod
    def get_css_dependencies(group):
        """
        Returns list of CSS dependencies belonging to `group` in settings.PIPELINE_JS.

        Respects `PIPELINE_ENABLED` setting.
        """
        if settings.PIPELINE_ENABLED:
            return [settings.PIPELINE_CSS[group]['output_filename']]
        else:
            return settings.PIPELINE_CSS[group]['source_filenames']

    @staticmethod
    def get_js_dependencies(group):
        """
        Returns list of JS dependencies belonging to `group` in settings.PIPELINE_JS.

        Respects `PIPELINE_ENABLED` setting.
        """
        if settings.PIPELINE_ENABLED:
            return [settings.PIPELINE_JS[group]['output_filename']]
        else:
            return settings.PIPELINE_JS[group]['source_filenames']

    @abstractmethod
    def vendor_js_dependencies(self):
        """
        Returns list of the vendor JS files that this view depends on.
        """
        return []

    @abstractmethod
    def js_dependencies(self):
        """
        Returns list of the JavaScript files that this view depends on.
        """
        return []

    @abstractmethod
    def css_dependencies(self):
        """
        Returns list of the CSS files that this view depends on.
        """
        return []

    def add_resource_urls(self, fragment):
        """
        Adds URLs for JS and CSS resources that this XBlock depends on to `fragment`.
        """
        # Head dependencies
        for vendor_js_file in self.vendor_js_dependencies():
            fragment.add_resource_url(staticfiles_storage.url(vendor_js_file), 'application/javascript', 'head')

        for css_file in self.css_dependencies():
            fragment.add_css_url(staticfiles_storage.url(css_file))

        # Body dependencies
        for js_file in self.js_dependencies():
            fragment.add_javascript_url(staticfiles_storage.url(js_file))

    def render_standalone_html(self, fragment):
        """
        Renders a standalone version of this fragment.
        """
        context = {
            'settings': settings,
            'fragment': fragment,
            'uses-pattern-library': self.USES_PATTERN_LIBRARY,
        }
        return render_to_response(settings.STANDALONE_FRAGMENT_VIEW_TEMPLATE, context)


class FragmentContainerView(View):
    """
    The base class of views that wrap a fragment.
    """

    @abstractmethod
    def render_fragment(self, request, **kwargs):
        """
        Not implemented yet.
        """
        raise NotImplementedError()

    @abstractmethod
    def render_fragment_to_string(self, request, fragment, **kwargs):
        """
        Renders the fragment to a string.
        """
        raise NotImplementedError()

    def render_fragment_to_response(self, request, **kwargs):
        """
        Renders a fragment to the HTTP response.

        This method renders a fragment either as an HTML or JSON response.

        Args:
            request: The Django request.
            **kwargs: Keyword arguments for render_fragment and render_fragment_to_string.

        Returns:
            HttpResponse: the HTTP response containing the fragment.
        """
        try:
            fragment = self.render_fragment(request, **kwargs)
            status_code = 200
        except Http404:
            raise  # re-raise 404s
        except Exception:  # pylint: disable=broad-except
            log.exception(u'Error rendering fragment')
            error_message = render_to_string('courseware/error-message.html', None)
            fragment = Fragment(error_message)
            status_code = 500

        response_format = request.GET.get('format') or request.POST.get('format') or 'html'
        if response_format == 'json' or WEB_FRAGMENT_RESPONSE_TYPE in request.META.get('HTTP_ACCEPT', 'text/html'):
            return JsonResponse(fragment.to_dict(), status=status_code)
        else:
            response_string = self.render_fragment_to_string(request, fragment, **kwargs)
            return HttpResponse(response_string, status=status_code)
