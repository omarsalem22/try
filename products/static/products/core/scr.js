inputs = document.querySelectorAll('input');
    textarea= document.querySelector('textarea')
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].classList.add('form-control');
    }
    textarea.classList.add('textarea', 'bg-slate-100', 'w-full')
    textarea.rows=1
    textarea.cols=30