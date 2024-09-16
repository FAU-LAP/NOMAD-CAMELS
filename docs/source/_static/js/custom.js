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