// Handle active state for navigation links
function handleClick(event) {
    console.log(`Link clicked: ${this.href}`); // Log the link URL

    // Remove active class from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    // Add active class to clicked link
    this.classList.add('active');
}

// Initialize and handle mobile sidebar functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the hamburger button for mobile using the specific ID
    const hamburgerBtn = document.getElementById('sidebarToggle');
    const sidebarMenu = document.getElementById('sidebarMenu');

    if (hamburgerBtn && sidebarMenu) {
        console.log('Sidebar toggle button and menu found');

        // Function to toggle the sidebar
        const toggleSidebar = function(event) {
            // Prevent default behavior
            event.preventDefault();
            event.stopPropagation();

            console.log('Toggle sidebar function called');

            // Toggle the 'show' class on the sidebar
            sidebarMenu.classList.toggle('show');

            // Update aria-expanded attribute
            const expanded = hamburgerBtn.getAttribute('aria-expanded') === 'true' || false;
            hamburgerBtn.setAttribute('aria-expanded', !expanded);

            console.log('Sidebar visibility toggled, show class:', sidebarMenu.classList.contains('show'));
        };

        // Direct toggle function that combines all approaches
        // This should work across all browsers and devices
        hamburgerBtn.onclick = function(event) {
            if (event) {
                event.preventDefault();
                event.stopPropagation();
            }

            console.log('Hamburger button clicked (direct toggle)');

            // Toggle the 'show' class
            sidebarMenu.classList.toggle('show');

            // Also directly manipulate the transform style as a fallback
            if (sidebarMenu.classList.contains('show')) {
                sidebarMenu.style.transform = 'translateX(0)';

                // Also show the navigation content inside the sidebar
                const navbarContent = document.getElementById('navbarContent');
                if (navbarContent) {
                    navbarContent.classList.add('show');
                    console.log('Navigation content shown');
                }
            } else {
                sidebarMenu.style.transform = 'translateX(-100%)';

                // Hide the navigation content when sidebar is hidden
                const navbarContent = document.getElementById('navbarContent');
                if (navbarContent) {
                    navbarContent.classList.remove('show');
                    console.log('Navigation content hidden');
                }
            }

            // Update aria-expanded attribute
            const expanded = hamburgerBtn.getAttribute('aria-expanded') === 'true' || false;
            hamburgerBtn.setAttribute('aria-expanded', !expanded);

            console.log('Sidebar visibility toggled, show class:', sidebarMenu.classList.contains('show'));
            console.log('Sidebar transform style:', sidebarMenu.style.transform);

            return false; // Ensure the event is fully canceled
        };

        // Enhanced touch event handling for mobile devices
        // Call the onclick function directly from touchstart for immediate response
        hamburgerBtn.addEventListener('touchstart', function(event) {
            console.log('Touch start event on hamburger button');
            // Call the onclick function directly
            hamburgerBtn.onclick(event);
        });

        // Prevent ghost clicks on touchend
        hamburgerBtn.addEventListener('touchend', function(event) {
            event.preventDefault();
            event.stopPropagation();
            console.log('Touch end event on hamburger button');
        });
    } else {
        console.error('Sidebar toggle button or menu not found');
        if (!hamburgerBtn) console.error('Hamburger button with ID "sidebarToggle" not found');
        if (!sidebarMenu) console.error('Sidebar menu with ID "sidebarMenu" not found');
    }

    // Function to close sidebar when interacting outside
    function closeSidebarIfOutside(event) {
        const sidebar = document.getElementById('sidebarMenu');
        const hamburgerBtn = document.getElementById('sidebarToggle');

        // If sidebar is open and interaction is outside sidebar and not on hamburger button
        if (sidebar && sidebar.classList.contains('show') && 
            !sidebar.contains(event.target) && 
            hamburgerBtn && !hamburgerBtn.contains(event.target)) {

            console.log('Interaction outside sidebar, closing it');

            // Hide the sidebar
            sidebar.classList.remove('show');
            sidebar.style.transform = 'translateX(-100%)';

            // Also hide the navigation content
            const navbarContent = document.getElementById('navbarContent');
            if (navbarContent) {
                navbarContent.classList.remove('show');
                console.log('Navigation content hidden (outside click)');
            }

            // Update hamburger button aria-expanded
            if (hamburgerBtn) {
                hamburgerBtn.setAttribute('aria-expanded', 'false');
            }
        }
    }

    // Add document click listener to close sidebar when clicking outside
    document.addEventListener('click', closeSidebarIfOutside);

    // Add document touchstart listener to close sidebar when touching outside (for mobile)
    document.addEventListener('touchstart', closeSidebarIfOutside);

    // Check if we're on a mobile device
    const isMobile = window.innerWidth < 768;

    // Ensure sidebar is initially hidden on mobile
    if (isMobile) {
        const sidebar = document.getElementById('sidebarMenu');
        if (sidebar) {
            // Make sure the sidebar is hidden initially on mobile
            sidebar.classList.remove('show');
            sidebar.style.transform = 'translateX(-100%)';

            // Also ensure navigation content is initially hidden
            const navbarContent = document.getElementById('navbarContent');
            if (navbarContent) {
                navbarContent.classList.remove('show');
                console.log('Ensuring navigation content is initially hidden on mobile');
            }

            console.log('Ensuring sidebar is initially hidden on mobile');
        }
        // Get all navigation links
        const navLinks = document.querySelectorAll('.nav-link');

        // Add click event listener to each link
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                // If this is a dropdown toggle, don't close the sidebar
                if (this.getAttribute('data-bs-toggle') === 'collapse') {
                    return;
                }

                // Get the sidebar element
                const sidebar = document.getElementById('sidebarMenu');

                // Simply remove the show class to hide the sidebar
                if (sidebar) {
                    console.log('Hiding sidebar after link click');
                    sidebar.classList.remove('show');

                    // Also update the aria-expanded attribute of the toggle button
                    const hamburgerBtn = document.getElementById('sidebarToggle');
                    if (hamburgerBtn) {
                        hamburgerBtn.setAttribute('aria-expanded', 'false');
                    }
                }
            });

            // Also handle touch events for mobile
            link.addEventListener('touchend', function(event) {
                // If this is a dropdown toggle, don't close the sidebar
                if (this.getAttribute('data-bs-toggle') === 'collapse') {
                    return;
                }

                // Prevent default only if it's not a link that should navigate
                if (this.getAttribute('href').startsWith('#')) {
                    event.preventDefault();
                }

                // Get the sidebar element
                const sidebar = document.getElementById('sidebarMenu');

                // Simply remove the show class to hide the sidebar
                if (sidebar) {
                    console.log('Hiding sidebar after link touch');
                    sidebar.classList.remove('show');

                    // Also update the aria-expanded attribute of the toggle button
                    const hamburgerBtn = document.getElementById('sidebarToggle');
                    if (hamburgerBtn) {
                        hamburgerBtn.setAttribute('aria-expanded', 'false');
                    }
                }
            });
        });
    }

    // Handle dropdown toggles for mobile
    const dropdownToggles = document.querySelectorAll('.nav-link.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        // Add touchend event listener for mobile
        toggle.addEventListener('touchend', function(event) {
            event.preventDefault();
            event.stopPropagation();

            console.log('Dropdown toggle touched');

            // Get the target collapse element
            const targetId = this.getAttribute('href');
            const targetCollapse = document.querySelector(targetId);

            if (targetCollapse) {
                // Toggle the collapse
                targetCollapse.classList.toggle('show');

                // Update aria-expanded attribute
                const expanded = this.getAttribute('aria-expanded') === 'true' || false;
                this.setAttribute('aria-expanded', !expanded);

                console.log('Dropdown toggled, show class:', targetCollapse.classList.contains('show'));
            }
        });
    });

    // Set active class based on current URL
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Handle window resize events (e.g., orientation changes on mobile)
    window.addEventListener('resize', function() {
        const sidebar = document.getElementById('sidebarMenu');
        const hamburgerBtn = document.getElementById('sidebarToggle');
        const navbarContent = document.getElementById('navbarContent');

        // Check if we're on mobile or desktop
        const isMobileNow = window.innerWidth < 768;

        if (sidebar) {
            if (isMobileNow) {
                // On mobile, ensure sidebar is hidden unless explicitly shown
                if (!sidebar.classList.contains('show')) {
                    sidebar.style.transform = 'translateX(-100%)';

                    // Also ensure navigation content is hidden
                    if (navbarContent) {
                        navbarContent.classList.remove('show');
                    }
                }
            } else {
                // On desktop, reset transform and show sidebar
                sidebar.style.transform = '';

                // On desktop, ensure navigation content is visible
                if (navbarContent) {
                    navbarContent.classList.add('show');
                }
            }

            console.log('Window resized, isMobile:', isMobileNow);
        }
    });
});
