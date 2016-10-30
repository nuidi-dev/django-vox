function computeTime(that) {
  var now = new Date();
  var d = new Date($(that).html())
  var computed = Math.abs(d-now);
  var c_sec = computed / 1000; // time in seconds

  if (c_sec < 60) {
    computed_text = "less than minute";
  } else if (c_sec / 60 < 60) {
    var compute_int = Math.floor(c_sec / 60);
    computed_text = compute_int.toString()+" minute";
  } else if (c_sec / 60 / 60 < 60) {
    var compute_int = Math.floor(c_sec / 60 / 60);
    computed_text = compute_int.toString()+" hour";
  } else if (c_sec / 60 / 60 / 24 < 30) {
    var compute_int = Math.floor(c_sec / 60 / 60 / 24);
    computed_text = compute_int.toString()+" day";
  } else if (c_sec / 60 / 60 / 24 / 30 > 1) {
    var compute_int = Math.floor(c_sec / 60 / 60 / 24);
    computed_text = compute_int.toString()+" month";
  }
  if (compute_int > 1) {
    computed_text+="s";
  }

  $(that).html(computed_text);
}
