Interceptor.attach(Module.findExportByName(null, 'open'), {
    onEnter: function (args) {
        this.path = Memory.readUtf8String(args[0]); 
    },
    onLeave: function (retval) {
        var fd = retval.toInt32(); 
        if (fd > 0) {
            var openedfile = this.path;
            send(openedfile);
        }
    }
});