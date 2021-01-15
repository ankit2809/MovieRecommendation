from django.shortcuts import render
from django.core.paginator import Paginator
#from .admin import TitlebasicsAdmin
from .models import Titlebasics,Titleratings,watchedmovie
from django.db.models import Q


# Create your views here.
def likemovies_index(request):
    show_full_result_count = False
    #moviename = Titlebasics.objects.using('sqlconn').raw('select tconst as id, titleType,originalTitle,endYear,genres from titlebasics LIMIT 10')
    #moviename = Titlebasics.objects.using('sqlconn').raw('select 1 id, tb.tconst, tb.titleType as titleType, tb.originalTitle as originalTitle, tb.startyear as startyear, tb.genres as genres from titleratings tr, titlebasics tb where tr.averageRating >9 and tr.tconst=tb.tconst order by tr.numVotes desc LIMIT 30')
    moviename = Titlebasics.objects.using('sqlconn').select_related('ratings').filter(ratings__averagerating__gte=8).filter(ratings__numvotes__gte=10000).filter(~Q(genres='None')).filter(titletype__in=('movie','tvSeries')) #filter(ratings__averagerating__gte=9).filter(ratings__numvotes__gte=10000)[0:100] 
    #moviename = Titlebasics.objects.using('sqlconn').all()[0:10]
    #for movie in moviename:
    #    print(moviename.originaltitle)
    #paginator = TitlebasicsAdmin(moviename, 10)
    #moviename.count('id')
    #moviename_query = [obj for obj in moviename[0:30]]
    #moviename_query = list(moviename)
    paginator = Paginator(moviename,15)
    #paginator._count = 100
    page_number = request.GET.get('page',1)
    page_obj = paginator.page(page_number)
    '''context = {

        'movietype' : titletype,
        'movietitle' : originaltitle,
        'year' : endyear,
        'genres' : genres

    }'''
    return render(request, 'helloworld.html', {'page_obj': page_obj})
    #return render(request, 'helloworld.html', {'movies':moviename})

'''def _get_count(self):
    "Returns the total number of objects, across all pages."
    if self._count is None:
        try:
            self._count = self.object_list.count()
        except (AttributeError, TypeError):
            # AttributeError if object_list has no count() method.
            # TypeError if object_list.count() requires arguments
            # (i.e. is of type list).
            self._count = len(self.object_list)
    return self._count
count = property(_get_count)
'''

def watchedcontent_result(request):
    item = watchedmovie()
    item.titleid=request.POST.get("movieid",False)
    item.watched=request.POST.get("watched_status",False)
    item.userid=request.META['REMOTE_ADDR']
    item.save(using='sqlconn')
    return render(request, 'helloworld.html')

def recommendations_result(request):
    show_full_result_count = False
    movierecommended = watchedmovie.objects.using('sqlconn').filter(userid=request.META['REMOTE_ADDR']).filter(~Q(watched='n')).exclude(recommended__isnull=True).values()
    list_recommend = []
    list_watched = []
    for i in range(len(movierecommended)):
        #print("##### My output :",movierecommended[i]['recommended'])
        list_watched.append(movierecommended[i]['titleid'])
        for movie in movierecommended[i]['recommended'].split(","):
            list_recommend.append(movie)
    sql = """select 1 id, tb.titleType as titleType, tb.originalTitle as originalTitle, tb.startyear as startyear, tb.genres as genres from titlebasics tb where tb.titleid in %s"""
    find_movies= Titlebasics.objects.using('sqlconn').filter(ratings__titleid__in=list_recommend).exclude(ratings__titleid__in=list_watched).filter(titletype__in=('movie','tvSeries'))
    paginator = Paginator(find_movies,15)
    page_number = request.GET.get('page',1)
    page_obj = paginator.page(page_number)
    return render(request, 'recommendationengine.html', {'page_obj': page_obj})