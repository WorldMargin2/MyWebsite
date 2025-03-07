(function(){
    $("._markdown").each(
        function(){
            var $this = $(this);
            $this.html(marked.parse($this.html()));
            $this.removeClass("_markdown");
        }
    );
})();