function toggleContent(event, element) {
    event.preventDefault(); // Prevent the default link action
    event.stopPropagation(); // Prevent the click from bubbling up to the anchor
    const content = element.previousElementSibling;
    if (content.classList.contains('expanded')) {
      content.classList.remove('expanded');
      element.textContent = 'More';
    } else {
      content.classList.add('expanded');
      element.textContent = 'Less';
    }
  }

  function filterFAQs() {
    let input = document.getElementById('searchInput').value.toLowerCase();
    let faqs = document.getElementsByClassName('box');

    for (let i = 0; i < faqs.length; i++) {
        let title = faqs[i].getElementsByClassName('box-title')[0];
        let content = faqs[i].getElementsByClassName('box-content')[0];
        let txtValue = title.textContent || title.innerText;
        txtValue += content.textContent || content.innerText;

        if (txtValue.toLowerCase().indexOf(input) > -1) {
            faqs[i].style.display = "";
        } else {
            faqs[i].style.display = "none";
        }
    }
}


// function toggleContent(element) {
//     let boxContent = element.parentElement.getElementsByClassName('box-content')[0];
//     boxContent.classList.toggle('expanded');
//     element.textContent = boxContent.classList.contains('expanded') ? 'Read Less' : 'Read More';
//     element.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
// }