document.addEventListener('DOMContentLoaded', function() {
  try {
    var tables = document.querySelectorAll('table');
    tables.forEach(function(tbl) {
      tbl.classList.add('table');
      tbl.classList.add('table-striped');
      tbl.classList.add('table-hover');
      tbl.classList.add('table-bordered');
      tbl.classList.add('table-sm');
    });
  } catch (e) {
    if (typeof console !== 'undefined' && console.warn) {
      console.warn('Table enhancement script error:', e);
    }
  }
});
