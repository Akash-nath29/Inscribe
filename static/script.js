let menuBar = document.querySelector('#createMenuBar');
let arrowDirection = document.querySelector('#arrowDirection');
menuBar.style.maxHeight = "0px";
function openMenuBar(){
    if(menuBar.style.maxHeight == "0px"){
        arrowDirection.innerHTML = '<svg id="upArrow" xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><style>#upArrow{fill:#494949; margin-left: 8vw;}</style><path d="M233.4 105.4c12.5-12.5 32.8-12.5 45.3 0l192 192c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L256 173.3 86.6 342.6c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3l192-192z"/></svg>';
        menuBar.style.maxHeight = "100px";
    }
    else {
        arrowDirection.innerHTML = '<svg id="downArrow" xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><style>#downArrow{fill:#494949;margin-left: 8vw;}</style><path d="M233.4 406.6c12.5 12.5 32.8 12.5 45.3 0l192-192c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L256 338.7 86.6 169.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l192 192z"/></svg>';
        menuBar.style.maxHeight = "0px";
    }
}
