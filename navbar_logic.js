var rotated = 0;
    function myFunction() {
      var x = document.getElementById("nav");
      if (x.style.display === "none") {
        x.style.display = "flex";
      }
      else {
        x.style.display = "none";
      }
    }
    function rotate() {
      var icon = document.getElementById('icon');
      if (rotated == 0) {
        icon.style.transform = 'rotate(90deg)';
        rotated = 1;
      }
      else {
        icon.style.transform = 'rotate(0deg)';
        rotated = 0;
      }
    }