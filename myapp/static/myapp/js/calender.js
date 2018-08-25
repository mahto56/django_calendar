function deleteCalenderEntry(entry){
    var $entry = $(entry)
    $(entry).parent().remove();
    var id = $entry.data('id');
    console.log(id)
    
    $.ajax({
        url: 'entry/delete/'+id,
        method: 'DELETE',
        beforeSend: function(xhr) {
            xhr.setRequestHeader('x-CSRFToken',csrf_token)
        }
    })
}


