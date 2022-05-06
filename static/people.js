function removeSpaces(val) {
    return val.split(' ').join('');
 }

 function onlySpaces(str) {
    return str.trim().length === 0;
  }


$(document).ready(function(){
    //when the page loads, display all the names
        
    $("#searchForm").submit(function(e){
        if (onlySpaces($("input").val()) == 1) {
            e.preventDefault()
            $("#search-bar").val('')
            $("#search-bar").focus()
            $("Form").attr(onsubmit="return false")
        } e.preventDefault()
    }) 

    $("#submit-btn").click(function(e){
        if (onlySpaces($("input").val()) == 1) {
            e.preventDefault()
            $("#search-bar").val('')
            $("#search-bar").focus()
            return false;   
        }  
        })
    
    
    $("#search-bar").keypress(function(e){     
        if(e.which == 13) {
            if (onlySpaces($("input").val()) == 1) {
                e.preventDefault()
                $("#search-bar").val('')
                $("#search-bar").focus()
                return false; 
            }
            }
        })
})