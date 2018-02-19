module.exports = function(grunt) {

  grunt.initConfig({
    copy: {
        jquery: {
            expand: true,
            cwd: 'node_modules/jquery/dist',
            src: ['jquery.min.js', 'jquery.min.map'],
            dest: '../dist'
        },
        bootstrap: {
            expand: true,
            cwd: 'node_modules/bootstrap/dist/css',
            src: ['bootstrap.min.css', 'bootstrap.min.css.map'],
            dest: '../dist'
        },
        sweetalert: {
            expand: true,
            cwd: 'node_modules/sweetalert2/dist',
            src: ['sweetalert2.all.min.js'],
            dest: '../dist'
        }
    },
  });

  require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

  grunt.registerTask('default', ['copy']);
};