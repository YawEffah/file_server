
//Automatically hide a message alert after 5seconds
document.addEventListener('DOMContentLoaded', (event) => {
    setTimeout(() => {
        const alert = document.querySelector('.sys-feedback');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
  });
  
  
  function w3_open() {
      document.getElementById("mySidebar").style.display = "block";
    }
    
  function w3_close() {
      document.getElementById("mySidebar").style.display = "none";
    }
  
  
  // Get the button:
  let topBtn = document.getElementById("topBtn");
  
  // When the user scrolls down 200px from the top of the document, show the button
  window.onscroll = function() {scrollFunction()};
  
  function scrollFunction() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 200) {
      topBtn.style.display = "block";
    } else {
      topBtn.style.display = "none";
    }
  }
  
  // When the user clicks on the button, scroll to the top of the document
  function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  }
  
  
  
  
  