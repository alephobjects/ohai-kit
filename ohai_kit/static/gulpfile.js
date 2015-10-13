'use strict';

var gulp = require('gulp'),
    sass = require('gulp-sass'),
    uglify = require('gulp-uglify'),
    paths = [
      './node_modules/breakpoint-sass/stylesheets',
      './node_modules/singularitygs/stylesheets'
    ];

gulp.task('styles', function() {
    gulp.src('./src/scss/**/*.scss')
        .pipe(sass({includePaths: paths}))
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./ohai_kit/'));
});

gulp.task('scripts', function() {
    gulp.src('./src/js/**/*.js')
    .pipe(uglify())
    .pipe(gulp.dest('./ohai_kit/'));
});

gulp.task('default',function() {
    gulp.watch('src/scss/**/*.scss',['styles']);
    gulp.watch('src/js/**/*.js',['scripts']);
});
