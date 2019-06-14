module.exports = function(grunt) {
  grunt.loadNpmTasks('grunt-contrib-copy')

  grunt.initConfig({
    copy: {
      all: {
        files: [
          {
            expand: true,
            cwd: 'node_modules',
            src: ['bootstrap/dist/**', 'jquery/dist/**', 'popper.js/dist/**'],
            dest: 'static/lib/'
          }
        ]
      }
    }
  })

  grunt.registerTask('go', ['copy'])
}
