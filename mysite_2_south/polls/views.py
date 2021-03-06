from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic

from polls.models import Choice, Poll


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """
        Return the last five published polls (not including those set to be
        published in the future).
        """
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DetailView, self).dispatch(*args, **kwargs)


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResultsView, self).dispatch(*args, **kwargs)


@login_required
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))