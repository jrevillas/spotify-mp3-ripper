sputrifis
=========

Sputrifis es un script escrito en Python con el que puedes descargar canciones y playlists enteras de Spotify. Ten en cuenta que Spotify no permite este tipo de descargas, utiliza este código bajo tu propia responsabilidad.

utilizando sputrifis
--------------------
    ./sputrifis.py [username] [password] [spotify_url]

ejemplos
--------
    ./sputrifis.py javirevillas 123456 spotify:track:0q6LuUqGLUiCPP1cbdwFs3
    ./sputrifis.py javirevillas 123456 spotify:user:aguarate:playlist:77sxS8MfEXMvgD1t5JikQq

características
---------------
* Descarga en tiempo real del stream PCM de Spotify.

* Incluye etiquetas ID3 en los archivos MP3.

* Descarga e incluye las portadas de los álbumes.

* Ubica los archivos siguiendo una estructura lógica de directorios.

dependencias
------------
* Spotify binary appkey - https://developer.spotify.com/

* libspotify - https://developer.spotify.com/technologies/libspotify/

* pyspotify - sudo pip install pyspotify

* lame - sudo apt-get install lame

* eyeD3 - sudo pip install eyeD3