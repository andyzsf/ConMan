from django.contrib import databrowse
from django.conf.urls.defaults import *
from voting.views import vote_on_object
from django.contrib.auth.decorators import user_passes_test
from common.models import LatestEntries #, LatestEntriesByCategory
from speakers.models import Presentation

#feeds = {
#    'latest': LatestEntries,
#    'categories': LatestEntriesByCategory,
#    'author': LatestEntriesByAuthor,
#}

presentation_dict = {
    'model': Presentation,
    'template_object_name': 'presentation',
    'allow_xmlhttprequest': True,
}
can_vote = user_passes_test(lambda u: u.has_perm('can_vote'))

urlpatterns = patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
#    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^accounts/', include('accounts.urls')),
#    (r'^profile/$', 'common.views.profile_show'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
#    (r'^volunteer/(?P<vol_id>\d+)?/?$', 'volunteers.views.index'),
    (r'^speaker/papers/(?P<abs_id>\d+)?/?$', 'speakers.views.abstract'),
    (r'^speaker/papers/(?P<abs_id>\d+)/delete/$', 'speakers.views.delete_abstract'),
    (r'^speaker/list/$', 'speakers.views.show_speakers'),
    (r'^speaker/(?P<s_id>\d+)/$', 'speakers.views.speaker_info'),
    (r'^presentation/(?P<p_id>\d+)/$', 'speakers.views.show_presentation'),
    (r'^presentation/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', can_vote(vote_on_object), presentation_dict),
#    (r'^speaker/$', 'speakers.views.index'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    (r'^$', 'common.views.index'),
)
