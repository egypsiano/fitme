// Add event listener to navigation links
document.querySelectorAll('nav a').forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();
    const target = event.target.getAttribute('href');
    document.querySelector(target).scrollIntoView({ behavior: 'smooth' });
  });
});

// Add event listener to section headings
document.querySelectorAll('h2').forEach(heading => {
  heading.addEventListener('click', event => {
    event.target.nextElementSibling.classList.toggle('open');
  });
});

// Add event listener to footer links
document.querySelectorAll('footer a').forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();
    const target = event.target.getAttribute('href');
    window.open(target, '_blank');
  });
});