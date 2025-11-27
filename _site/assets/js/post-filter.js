// Post filtering functionality
(function() {
  'use strict';
  
  // Wait for DOM to be ready
  document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter');
    const posts = document.querySelectorAll('.post');
    
    if (filterButtons.length === 0 || posts.length === 0) {
      return;
    }
    
    // Add click event to each filter button
    filterButtons.forEach(function(button) {
      button.addEventListener('click', function() {
        const filter = this.getAttribute('data-filter');
        
        // Update active state
        filterButtons.forEach(function(btn) {
          btn.classList.remove('active');
        });
        this.classList.add('active');
        
        // Filter posts
        posts.forEach(function(post) {
          if (filter === 'all') {
            post.style.display = 'block';
          } else if (filter.startsWith('lang-')) {
            const lang = filter.replace('lang-', '');
            if (post.getAttribute('data-lang') === lang) {
              post.style.display = 'block';
            } else {
              post.style.display = 'none';
            }
          } else if (filter.startsWith('cat-')) {
            const category = filter.replace('cat-', '');
            if (post.getAttribute('data-category') === category) {
              post.style.display = 'block';
            } else {
              post.style.display = 'none';
            }
          }
        });
        
        // Smooth animation
        const postsContainer = document.querySelector('.posts');
        if (postsContainer) {
          postsContainer.style.opacity = '0.5';
          setTimeout(function() {
            postsContainer.style.opacity = '1';
          }, 150);
        }
      });
    });
  });
})();
