# -*- coding: utf-8 -*-
from urllib.parse import urlparse
try:
	from urlparse import parse_qsl
except:
	from urllib.parse import parse_qsl

import sys

params = dict(parse_qsl(sys.argv[2].replace('?','').replace(';+','')))
import xbmc
#xbmc.log(str(params)+'===>PHIL', level=xbmc.LOGINFO)

action = params.get('action')

icon = params.get('icon')

id = params.get('id')

type = params.get('type')

name = params.get('name')

title = params.get('title')

year = params.get('year')

imdb = params.get('imdb')

tvdb = params.get('tvdb')

tmdb = params.get('tmdb')

season = params.get('season')
plot = params.get('plot')

episode = params.get('episode')

tvshowtitle = params.get('tvshowtitle')

premiered = params.get('premiered')

url = params.get('url')

image = params.get('image')

meta = params.get('meta')


try:
	test_var = meta['poster']
except:
	try:
		meta2 = {}
		for i in meta.split('", "'):
			if 'tmdb":' in i or 'imdb":' in i:
				meta2[i.split(':')[0].replace('"','').replace('}','').replace('{','')] = i.split(':')[1].split(', "')[0].replace(' ','')
				meta2[i.split(':')[1].split(', "')[1].replace('"','').replace('}','').replace('{','')] = i.split(':')[2].replace('"','').replace('}','').replace('{','').replace(' ','')
#			elif 'plot":' in i:
#				xbmc.log(str(i)+'===>PHIL', level=xbmc.LOGINFO)
			else:
				meta2[i.split(': "')[0].replace('"','').replace('}','').replace('{','')] = i.split(': "')[1].replace('"','').replace('}','').replace('{','')
			meta = meta2
	except:
		pass

select = params.get('select')

query = params.get('query')

source = params.get('source')

content = params.get('content')

clearlogo = params.get('clearlogo')


#xbmc.log(str(params)+'===>REALIZER', level=xbmc.LOGINFO)
if  params.get('content') == 'movie' and (clearlogo == '' or clearlogo == ' ' or clearlogo == None):
	import requests,json
	title = title
	year = year
	if tmdb == ' ' or tmdb == '' or tmdb == None:
		response = requests.get('https://api.themoviedb.org/3/search/movie?api_key=2cfb516815547f7a9fb865409fe94da2&query='+str(title)+'&language=en-US&include_image_language=en,null&year='+str(year)).json()
		tmdb = response['results'][0]['id']
		response = requests.get('https://api.themoviedb.org/3/movie/'+str(tmdb)+'?api_key=2cfb516815547f7a9fb865409fe94da2&language=en-US').json()
		for i in response:
			if 'overview' in i:
				plot = response[i]
				plot = str(plot).replace('"','')


	response = requests.get('http://webservice.fanart.tv/v3/movies/'+str(tmdb)+'?api_key=77cf47921f757933c6ea635af10710c7&client_key=50f0202231883f1be2f746870f87b343').json()
	for i in response['hdmovielogo']:
		if i['lang'] == 'en':
			url = i['url']
			clearlogo = url
			break
#xbmc.log(str(clearlogo)+'===>REALIZER', level=xbmc.LOGINFO)

if 	str(season) is not None and str(episode) is not None:
	flag_tmdb = True
else:
	flag_tmdb = False

xbmc.log(str(params)+'===>REALIZER', level=xbmc.LOGINFO)
if params.get('content') == 'episode' and flag_tmdb == True or ((tvshowtitle  != '' and tvshowtitle != None and tvshowtitle != ' ') and (clearlogo == '' or clearlogo == ' ' or clearlogo == None)):
	import requests,json
	title = tvshowtitle
	if  flag_tmdb == True or (tvdb == ' ' or tvdb == '' or tvdb == None):
		response = requests.get('https://api.themoviedb.org/3/search/tv?api_key=2cfb516815547f7a9fb865409fe94da2&query='+str(title)+'&language=en-US&include_image_language=en,null').json()
		tmdb = response['results'][0]['id']
		#xbmc.log(str(response)+'TMDB===>PHIL', level=xbmc.LOGINFO)
		response = requests.get('https://api.themoviedb.org/3/tv/'+str(tmdb)+'/season/'+str(season)+'/episode/'+str(episode)+'?api_key=2cfb516815547f7a9fb865409fe94da2&language=en-US').json()
		for i in response:
			if 'overview' in i:
				plot = response[i].replace('"','')
				#plot = str(plot.encode('utf-8', errors='ignore')).replace('"','')
				#xbmc.log(str(i)+'TMDB===>PHIL', level=xbmc.LOGINFO)
				#xbmc.log(str(response[i])+'TMDB===>PHIL', level=xbmc.LOGINFO)
		
		#plot = str(response['overview']).replace('"','')

		try:
			meta = meta.replace('plot": "', str('plot":' +str(plot) +  '"'))
		except: 
			pass

		
		response = requests.get('https://api.themoviedb.org/3/tv/'+str(tmdb)+'/external_ids?api_key=2cfb516815547f7a9fb865409fe94da2').json()
		tvdb =  response['tvdb_id']


	response = requests.get('http://webservice.fanart.tv/v3/tv/'+str(tvdb)+'?api_key=77cf47921f757933c6ea635af10710c7&client_key=50f0202231883f1be2f746870f87b343').json()
	url = ''
	for i in response['hdtvlogo']:
		if i['lang'] == 'en':
			url = i['url']
			clearlogo = url
			break
	if url == '':
		for i in response['clearlogo']:
			if i['lang'] == 'en':
				url = i['url']
				clearlogo = url
				break
#xbmc.log(str(clearlogo)+'===>REALIZER', level=xbmc.LOGINFO)

page = params.get('page')

#xbmc.log(str(plot)+'===>PHIL', level=xbmc.LOGINFO)
#xbmc.log(str(action)+'===>PHIL', level=xbmc.LOGINFO)

#try:
#	if meta:
#		xbmc.log(str(meta)+'===>PHIL', level=xbmc.LOGINFO)
#except:
#	meta = None

#xbmc.log(str(title)+'===>PHIL', level=xbmc.LOGINFO)
#xbmc.log(str(year)+'===>PHIL', level=xbmc.LOGINFO)
#xbmc.log(str(imdb)+'===>PHIL', level=xbmc.LOGINFO)
#xbmc.log(str(tvdb)+'===>PHIL', level=xbmc.LOGINFO)
#xbmc.log(str(season)+'===>PHIL', level=xbmc.LOGINFO)
#xbmc.log(str(episode)+'===>PHIL', level=xbmc.LOGINFO)
#xbmc.log(str(tvshowtitle)+'===>PHIL', level=xbmc.LOGINFO)
#xbmc.log(str(premiered)+'===>PHIL', level=xbmc.LOGINFO)
#xbmc.log(str(meta)+'===>PHIL', level=xbmc.LOGINFO)
#xbmc.log(str(clearlogo)+'===>PHIL', level=xbmc.LOGINFO)
#xbmc.log(str(plot)+'===>PHIL', level=xbmc.LOGINFO)



if action == None:

	# from resources.lib.modules import changelog
	# changelog.get()

	from resources.lib.indexers import navigator
	navigator.navigator().root()

elif action == 'donations':
	import xbmcaddon
	from resources.lib.modules import deviceAuthDialog
	authDialog = deviceAuthDialog.DonationDialog('donations.xml', xbmcaddon.Addon().getAddonInfo('path'), code='', url='')
	authDialog.doModal()
	del authDialog

elif action == 'browse_nav':
	from resources.lib.indexers import navigator
	navigator.navigator().browse_nav()

elif action == 'play':
	#xbmc.log(str(season)+'TMDB1===>PHIL', level=xbmc.LOGINFO)
	#xbmc.log(str(title)+'TMDB1===>PHIL', level=xbmc.LOGINFO)
	from resources.lib.sources import sources
	sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, clearlogo, plot)

elif action == 'directPlay':
	from resources.lib.sources import sources
	#xbmc.log(str(season)+'TMDB2===>PHIL', level=xbmc.LOGINFO)
	#xbmc.log(str(episode)+'TMDB2===>PHIL', level=xbmc.LOGINFO)
	sources().directPlay(url, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, id, name, clearlogo, plot)

elif action == 'authRealdebrid':
	from resources.lib.modules import control
	from resources.lib.api import debrid
	token = debrid.realdebrid().auth()


elif action == 'testItem':
	from resources.lib.api import fanarttv
	imdb = '121361'
	query = 'tv'
	fanarttv.get(imdb, query)
elif action == 'testSources':
	from resources.lib.sources import sources
	sources().advtestmode()

elif action == 'nextaired':
	from resources.lib.api import tvdbapi
	tvdbapi.airingtoday().get()

elif action == 'helpNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().help()

elif action == 'changelogNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().changelog()

elif action == 'meta_cloud':
	from resources.lib.indexers import navigator
	navigator.navigator().meta_cloud()

elif action == 'meta_folder':
	from resources.lib.api import debrid
	debrid.meta_folder(content=content)

elif action == 'meta_episodes':
	from resources.lib.api import debrid
	debrid.meta_episodes(imdb=imdb, tvdb=tvdb, tmdb=tmdb)


# PREMIUMIZE SECTION #################
elif action == 'rdNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().rdNav()

elif action == 'rdTransfers':
	from resources.lib.api import debrid
	debrid.transferList(page=page)

elif action == 'rdTorrentList':
	from resources.lib.api import debrid
	debrid.torrentList(page=page)

elif action == 'playtorrentItem':
	from resources.lib.api import debrid
	debrid.playtorrentItem(name, id)

elif action == 'rdTorrentInfo':
	from resources.lib.api import debrid
	debrid.torrentInfo(id)

elif action == 'rdAddTorrent':
	from resources.lib.api import debrid
	import urllib
	id = urllib.unquote_plus(id)
	debrid.addTorrent(id)

elif action == 'rdDeleteAll':
	from resources.lib.modules import control
	from resources.lib.api import debrid
	debrid.realdebrid().delete('0', deleteAll=True)
	control.refresh()

elif action == 'rdDeleteItem':
	from resources.lib.modules import control
	from resources.lib.api import debrid
	debrid.realdebrid().delete(id, type=type)
	control.refresh()

elif action == 'rss_manager':
	from resources.lib.modules import rss
	rss.manager()

elif action == 'rss_manager_nav':
	from resources.lib.indexers import navigator
	navigator.navigator().rss_manager_nav()

elif action == 'rss_reader_cat':
	from resources.lib.modules import rss
	rss.reader_cat()

elif action == 'rss_reader':
	from resources.lib.modules import rss
	rss.reader(id)

elif action == 'rss_update':
	from resources.lib.modules import rss
	rss.update()

elif action == 'rss_clear':
	import os
	from resources.lib.modules import control
	try: os.remove(control.rssDb)
	except:pass
	try: os.remove(control.rssDb)
	except:pass
	control.refresh()

elif action == 'realizerootFolder':
	from resources.lib.api import premiumize
	premiumize.getFolder('root')

elif action == 'downloadFolder':
	from resources.lib.api import premiumize
	premiumize.downloadFolder(name, id)

elif action == 'downloadZip':
	from resources.lib.api import premiumize
	premiumize.downloadFolder(name, id)

elif action == 'realizerename':
	from resources.lib.api import premiumize
	premiumize.renameItem(title, id, type)

elif action == 'getSearchMovie':
	from resources.lib.indexers import movies
	movies.movies().getSearch(create_directory=True)

elif action == 'addToLibrary':
	from resources.lib.api import premiumize
	premiumize.addtolibrary_service(id=id, type=type, name=name)


elif action == 'forcecloudsync':
	from resources.lib.modules import updater
	updater.updatelibrary()

elif action == 'service':
	from resources.lib.modules import control
	if control.setting('rss.1') == 'true' or control.setting('rss.2') == 'true' or control.setting('rss.3') == 'true' or control.setting('rss.4') == 'true':
		from resources.lib.modules import rss
		rss.update()

elif action == 'play_library':
	from resources.lib.api import premiumize
	premiumize.library_play().play(name, id)

elif action == 'selectivelibrary_nav':
	from resources.lib.api import premiumize
	premiumize.selectivelibrary_nav()

elif action == 'selectiveLibraryManager':
	from resources.lib.api import premiumize
	premiumize.selectiveLibraryManager(id, name)


elif action == 'tvdbFav':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().getTvdbFav()

elif action == 'tvdbAdd':
	from resources.lib.api import tvdbapi
	tvdbapi.addTvShow(tvshowtitle, tvdb)

elif action == 'tvdbRemove':
	from resources.lib.api import tvdbapi
	tvdbapi.removeTvShow(tvdb)

elif action == 'AuthorizeTvdb':
	from resources.lib.api import tvdbapi
	tvdbapi.forceToken()

elif action == 'updateAddon':
	from resources.lib.modules import updater
	updater.update_addon()

elif action == 'updateSources':
	from resources.lib.modules import updater
	updater.update_sources()

elif action == 'firstSetup':
	from resources.lib.modules import setupTools
	setupTools.FirstStart()



elif action == 'movieFavourites':
	from resources.lib.indexers import movies
	movies.movies().favourites()

elif action == 'remoteManager':
	from resources.lib.api import remotedb
	if content == 'movie': remotedb.manager(imdb, tmdb, meta, content)
	else: remotedb.manager(imdb, tvdb, meta, content)

elif action == 'remotelibrary_movies':
	from resources.lib.api import remotedb
	remotedb.getMovies()

elif action == 'remotelibrary_tv':
	from resources.lib.api import remotedb
	remotedb.getTV()

elif action == 'tvFavourites':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().favourites()

elif action == 'addFavourite':
	from resources.lib.modules import favourites
	favourites.addFavourite(meta, content)

elif action == 'deleteFavourite':
	from resources.lib.modules import favourites
	favourites.deleteFavourite(meta, content)

elif action == 'moviesInProgress':
	from resources.lib.indexers import movies
	movies.movies().inProgress()

elif action == 'tvInProgress':
	from resources.lib.indexers import episodes
	episodes.episodes().inProgress()

elif action == 'deleteProgress':
	from resources.lib.modules import favourites
	favourites.deleteProgress(meta, content)

elif action == 'movieNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().movies()

elif action == 'movieliteNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().movies(lite=True)

elif action == 'mymovieNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().mymovies()

elif action == 'mymovieliteNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().mymovies(lite=True)

elif action == 'tvNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().tvshows()

elif action == 'tvliteNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().tvshows(lite=True)

elif action == 'mytvNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().mytvshows()

elif action == 'mytvliteNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().mytvshows(lite=True)

elif action == 'downloadNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().downloads()

elif action == 'libraryNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().library()



elif action == 'toolNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().tools()

elif action == 'searchNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().search()

elif action == 'viewsNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator().views()

elif action == 'clearCache':
	from resources.lib.modules import control
	from resources.lib.modules import cache
	cache.cache_clear()
	control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

elif action == 'infoCheck':
	from resources.lib.indexers import navigator
	navigator.navigator().infoCheck('')

elif action == 'movies':
	from resources.lib.indexers import movies
	movies.movies().get(url)

elif action == 'moviePage':
	from resources.lib.indexers import movies
	movies.movies().get(url)

elif action == 'movieWidget':
	from resources.lib.indexers import movies
	movies.movies().widget()

elif action == 'movieSearch':
	from resources.lib.indexers import movies
	movies.movies().search()

elif action == 'moviePerson':
	from resources.lib.indexers import movies
	movies.movies().person()

elif action == 'movieGenres':
	from resources.lib.indexers import movies
	movies.movies().genres()

elif action == 'movieLanguages':
	from resources.lib.indexers import movies
	movies.movies().languages()

elif action == 'movieCertificates':
	from resources.lib.indexers import movies
	movies.movies().certifications()

elif action == 'movieYears':
	from resources.lib.indexers import movies
	movies.movies().years()

elif action == 'moviePersons':
	from resources.lib.indexers import movies
	movies.movies().persons(url)

elif action == 'movieUserlists':
	from resources.lib.indexers import movies
	movies.movies().userlists()

elif action == 'channels':
	from resources.lib.indexers import channels
	channels.channels().get()

elif action == 'tvshows':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().get(url)

elif action == 'tvshowsTvdb':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().getTvdb(url)


elif action == 'tvshowPage':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().get(url)

elif action == 'tvSearch':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().search()

elif action == 'tvSearchTvdb':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().searchTvdb()

elif action == 'tvPerson':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().person()

elif action == 'tvGenres':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().genres()

elif action == 'tvNetworks':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().networks()

elif action == 'tvLanguages':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().languages()

elif action == 'tvCertificates':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().certifications()

elif action == 'tvPersons':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().persons(url)

elif action == 'tvUserlists':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().userlists()

elif action == 'seasons':
	from resources.lib.indexers import episodes
	episodes.seasons().get(tvshowtitle, year, imdb, tvdb)

elif action == 'episodes':
	from resources.lib.indexers import episodes
	episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, episode)

elif action == 'calendar':
	from resources.lib.indexers import episodes
	episodes.episodes().calendar(url)

elif action == 'traktOnDeck':
	if content == 'movies':
		from resources.lib.indexers import movies
		movies.movies().traktOnDeck()

elif action == 'tvWidget':
	from resources.lib.indexers import episodes
	episodes.episodes().widget()

elif action == 'calendars':
	from resources.lib.indexers import episodes
	episodes.episodes().calendars()

elif action == 'episodeUserlists':
	from resources.lib.indexers import episodes
	episodes.episodes().userlists()

elif action == 'refresh':
	from resources.lib.modules import control
	control.refresh()

elif action == 'queueItem':
	from resources.lib.modules import control
	control.queueItem()

elif action == 'openSettings':
	from resources.lib.modules import control
	control.openSettings(query)

elif action == 'artwork':
	from resources.lib.modules import control
	control.artwork()

elif action == 'addView':
	from resources.lib.modules import views
	views.addView(content)

elif action == 'moviePlaycount':
	from resources.lib.modules import playcount
	playcount.movies(imdb, query)

elif action == 'episodePlaycount':
	from resources.lib.modules import playcount
	playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
	from resources.lib.modules import playcount
	playcount.tvshows(name, imdb, tvdb, season, query)

elif action == 'trailer':
	from resources.lib.modules import trailer
	trailer.trailer().play(name, url)

elif action == 'traktManager':
	from resources.lib.api import trakt
	trakt.manager(name, imdb, tvdb, content)

#elif action == 'authTrakt':
	#from resources.lib.api import trakt
	#trakt.authTrakt()
#
elif action == 'download':
	from resources.lib.api import debrid
	debrid.downloadItem(name, url, id)

elif action == 'download_manager':
	from resources.lib.indexers import navigator
	navigator.navigator().download_manager()

elif action == 'download_manager_list':
	from resources.lib.modules import downloader
	downloader.downloader().download_manager()



elif action == 'download_manager_stop':

	from resources.lib.modules import downloader, control
	downloader.downloader().logDownload(title, '0', '0', mode='stop')
	control.refresh()

elif action == 'download_manager_delete':
	from resources.lib.modules import downloader, control
	downloader.downloader().logDownload(title, '0', '0', mode='delete')
	control.refresh()

elif action == 'addItem':
	from resources.lib.sources import sources
	sources().addItem(title)

elif action == 'playItem':
	from resources.lib.sources import sources
	sources().playItem(title, source)

elif action == 'alterSources':
	from resources.lib.sources import sources
	sources().alterSources(url, meta)

elif action == 'clearSources':
	from resources.lib.sources import sources
	sources().clearSources()

elif action == 'clearMeta':
	import os
	from resources.lib.modules import control
	control.idle()
	try: os.remove(control.cacheFile)
	except:pass
	try: os.remove(control.metacacheFile)
	except:pass

	control.infoDialog('Meta Cache Deleted', sound=True, icon='INFO')

elif action == 'backupSettings':
	from resources.lib.modules import updater
	updater.backupAddon()

elif action == 'restoreSettings':
	from resources.lib.modules import updater
	updater.restoreAddon()
