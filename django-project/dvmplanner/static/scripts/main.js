function toggleNavbar() {
  const navbar = document.getElementById('navbar');
  const content = document.getElementById('content');
  navbar.classList.toggle('shown_navbar');
  content.classList.toggle('hidden_content');
}