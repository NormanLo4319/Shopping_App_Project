function preview(event){
    var input = event.target.files[0];
    var reader = new FileReader();
    reader.onload = function(){
      var result = reader.result;
      var img = document.getElementById('photo');
      img.src = result;
    }
    reader.readAsDataURL(input);
  }