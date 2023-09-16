$(document).ready(function() {
  // Function to read the URL of the uploaded image and display it in the image element
  function readURL(input, displayElement) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function(e) {
        console.log("File read successfully.");
        console.log("Base64 Data URL:", e.target.result); // Debug statement
        $(displayElement).attr('src', e.target.result);
        originalImageData = e.target.result; // Store the original image data
      }

      console.log("Reading file...");
      reader.readAsDataURL(input.files[0]); // convert to base64 string
    } else {
      // If no image selected, display the default image
      var defaultSrc = $(displayElement).data('default-src');
      $(displayElement).attr('src', defaultSrc);
      originalImageData = defaultSrc; // Store the default image data as the original image data
    }
  }

  // Event handler for the image input change
  $("#image").change(function() {
    console.log("NFT Image file input changed.");
    readURL(this, '#display_nftimage');
  });

  // Event handler for the "Remove Image" button
  $("#remove-image-btn").click(function() {
    var defaultSrc = $("#display_nftimage").data('default-src');
    $("#display_nftimage").attr('src', defaultSrc);
    $("#image").val(''); // Clear the file input value to reset it
  });


  // Display the default image when the page loads
  var defaultSrc = $("#display_nftimage").data('default-src');
  originalImageData = defaultSrc; // Store the original image data
  $("#display_nftimage").attr('src', defaultSrc);
  });