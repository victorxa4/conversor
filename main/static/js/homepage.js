document.querySelector('.container form input[name="image"]').addEventListener('click', e => {
    var image_format = document.querySelector('.container form select[name="image_format"]').value
    var target_format = document.querySelector('.container form select[name="target_format"]').value

    if (image_format && target_format && image_format != target_format) {
        e.target.accept = 'image/' + image_format
    } else {
        e.preventDefault()
    }
})