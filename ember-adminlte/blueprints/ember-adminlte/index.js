/*jshint node:true*/
module.exports = {
    normalizeEntityName: function() {
    },

  // locals: function(options) {
  //   // Return custom template variables here.
  //   return {
  //     foo: options.entity.options.foo
  //   };
  // }

  afterInstall: function(options) {
    return this.addBowerPackageToProject('bootstrap', '~3.3.5').then(function() {
        return this.addBowerPackageToProject('font-awesome', '~4.4.0').then(function() {
            return this.addBowerPackageToProject('admin-lte', '~2.3.2');
        }.bind(this));
    }.bind(this));
  }
};
