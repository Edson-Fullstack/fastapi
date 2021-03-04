[% extends "/components/.vue" %]
[%block content %]

var app =new Vue({
        el: '#app',
        data: {message: [[teste | tojson ]]}
    })
[% endblock %]