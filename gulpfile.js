'use strict';

var gulp = require('gulp'),
    watch = require('gulp-watch'),
    prefixer = require('gulp-autoprefixer'),
    uglify = require('gulp-uglify'),
    sass = require('gulp-sass'),
    sourcemaps = require('gulp-sourcemaps'),
    rigger = require('gulp-rigger'),
    cssmin = require('gulp-minify-css'),
    imagemin = require('gulp-imagemin'),
    pngquant = require('imagemin-pngquant'),
    rimraf = require('rimraf'),
    browserSync = require("browser-sync"),
    reload = browserSync.reload;

var path = {
    build: {
        js: 'templates/public/js/',
        css: 'templates/public/css/'
    },
    src: {
        js: 'gulp/js/main.js',
        style: 'gulp/style/main.sass'
    },
    watch: {
        js: 'gulp/js/*.js',
        style: 'gulp/style/*.sass'
    },
    clean: './build'
};




gulp.task('clean', function (cb) {
    rimraf(path.clean, cb);
});


gulp.task('js:build', function () {
    gulp.src(path.src.js)
        .pipe(rigger())
        // .pipe(sourcemaps.init())
        .pipe(uglify().on('error', function(e){
            console.log(e);
         }))
        // .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.build.js))

});

gulp.task('style:build', function () {
    gulp.src(path.src.style)
        // .pipe(sourcemaps.init())
        .pipe(sass({
            includePaths: ['src/style/'],
            outputStyle: 'compressed',
            sourceMap: true,
            errLogToConsole: true
        }))
        .pipe(prefixer())
        .pipe(cssmin())
        // .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.build.css))

});



gulp.task('build', [
    'js:build',
    'style:build'
]);


gulp.task('watch', function(){

    watch([path.watch.style], function(event, cb) {
        gulp.start('style:build');
    });
    watch([path.watch.js], function(event, cb) {
        gulp.start('js:build');
    });

});


gulp.task('default', ['build', 'watch']);