// Post filtering functionality
(function() {
  'use strict';
  
  // Wait for DOM to be ready
  document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const postCards = document.querySelectorAll('.post-card');
    
    if (filterButtons.length === 0 || postCards.length === 0) {
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
        postCards.forEach(function(card) {
          if (filter === 'all') {
            card.classList.remove('hidden');
          } else if (filter.startsWith('lang-')) {
            const lang = filter.replace('lang-', '');
            if (card.getAttribute('data-lang') === lang) {
              card.classList.remove('hidden');
            } else {
              card.classList.add('hidden');
            }
          } else if (filter.startsWith('cat-')) {
            const category = filter.replace('cat-', '');
            if (card.getAttribute('data-category') === category) {
              card.classList.remove('hidden');
            } else {
              card.classList.add('hidden');
            }
          }
        });
        
        // Smooth scroll animation
        const postGrid = document.querySelector('.post-grid');
        if (postGrid) {
          postGrid.style.opacity = '0.5';
          setTimeout(function() {
            postGrid.style.opacity = '1';
          }, 150);
        }
      });
    });
  });
})();
