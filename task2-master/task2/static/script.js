$(document).ready(function() {
    //toggle check on/off for all checkboxes
    $("#check_all").click(function(){
        $('input:checkbox').not(this).prop('checked', this.checked);
    });

    $('#remove').click(function (){
        //bucket for checked ids
        var strconfirm = confirm("Are you sure you?");

        if(strconfirm == true){
            var comicslist = [];
            $('.checkboxes:checkbox:checked').each(function () {
                    if(this.checked && $(this).val() != 'on'){
                        comicslist.push($(this).val());
                    }
            });
            //post for the removal of the document
            $.post('/remove',{'data[]': comicslist}, function(result){
                console.log(result)
            });
        }

        //so id doesn't redirect
        return false;
    });
});
