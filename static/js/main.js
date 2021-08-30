const player = new Plyr('#player', {
   title: 'Example Title',
});

videojs('#example_video_1', {}, function () { });

$('.player3').mediaelementplayer({
   // Do not forget to put a final slash (/)
   pluginPath: 'https://cdnjs.com/libraries/mediaelement/',
   // this will allow the CDN to use Flash without restrictions
   // (by default, this is set as `sameDomain`)
   shimScriptAccess: 'always'
   // more configuration
});
