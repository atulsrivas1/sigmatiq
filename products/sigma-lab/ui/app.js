
import { render as renderDashboard } from './views/dashboard.js';
import { render as renderPacks } from './views/packs.js';
import { render as renderModels } from './views/models.js';
import { render as renderModelCreate } from './views/model-create.js';
import { render as renderModelDesigner } from './views/model-designer.js';
import { render as renderModelComposer } from './views/model-composer.js';
import { render as renderSignals } from './views/signals.js';
import { render as renderOverlay } from './views/overlay.js';
import { render as renderHealth } from './views/health.js';
import { render as renderDocs } from './views/docs.js';
import { render as renderAdmin } from './views/admin.js';

document.addEventListener('DOMContentLoaded', () => {
    const app = document.getElementById('app');
    const root = document.documentElement;
    const sidebar = document.getElementById('sidebar');
    const menuBtn = document.getElementById('menu-toggle-btn');

    // --- Theme and Density --- 
    const ls = window.localStorage;
    const themeBtn = document.getElementById('themeBtn');
    const densitySelect = document.getElementById('densitySelect');
    
    const applyTheme = (theme) => { root.dataset.theme = theme; ls.setItem('ui.theme', theme); };
    const applyDensity = (density) => { root.dataset.density = density; ls.setItem('ui.density', density); };
    
    themeBtn.addEventListener('click', () => {
        const order = ['light', 'dark', 'slate', 'paper'];
        const next = order[(order.indexOf(root.dataset.theme) + 1) % order.length];
        applyTheme(next);
    });
    
    densitySelect.addEventListener('change', (e) => {
        applyDensity(e.target.value);
    });
    
    const savedTheme = ls.getItem('ui.theme');
    const savedDensity = ls.getItem('ui.density');
    
    applyTheme(savedTheme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
    applyDensity(savedDensity || 'cozy');
    
    // Update density select to match current value
    densitySelect.value = root.dataset.density;
    
    // --- Risk Profile Management ---
    const riskProfileChips = document.getElementById('riskProfileChips');
    let currentRiskProfile = ls.getItem('ui.riskProfile') || 'balanced';
    
    function updateRiskProfile(profile) {
        currentRiskProfile = profile;
        ls.setItem('ui.riskProfile', profile);
        document.querySelectorAll('.risk-chip').forEach(chip => {
            chip.classList.toggle('active', chip.dataset.profile === profile);
        });
        // Dispatch custom event for components to listen to
        window.dispatchEvent(new CustomEvent('riskProfileChanged', { detail: { profile } }));
    }
    
    // Initialize risk profile
    updateRiskProfile(currentRiskProfile);
    
    // Risk profile chip event listeners
    riskProfileChips.addEventListener('click', (e) => {
        if (e.target.classList.contains('risk-chip')) {
            updateRiskProfile(e.target.dataset.profile);
        }
    });
    
    // Expose risk profile globally
    window.getCurrentRiskProfile = () => currentRiskProfile;

    // --- Expandable Navigation ---
    function initExpandableNavigation() {
        const navParents = document.querySelectorAll('.nav-parent');
        
        navParents.forEach(parent => {
            parent.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                // Don't expand if sidebar is collapsed
                if (sidebar.classList.contains('collapsed')) {
                    return;
                }
                
                const toggleId = parent.getAttribute('data-toggle');
                const submenu = document.getElementById(`${toggleId}-submenu`);
                const chevron = parent.querySelector('.nav-chevron');
                const isNested = parent.closest('.nav-nested');
                
                if (submenu) {
                    const isExpanded = submenu.classList.contains('expanded');
                    
                    // For nested menus, only close other nested menus in the same parent
                    // For top-level menus, close all other top-level menus
                    if (isNested) {
                        // Close other nested submenus in the same parent
                        const parentSubmenu = parent.closest('.nav-submenu');
                        if (parentSubmenu) {
                            parentSubmenu.querySelectorAll('.nav-nested-submenu.expanded').forEach(menu => {
                                if (menu !== submenu) {
                                    menu.classList.remove('expanded');
                                    const otherParent = parentSubmenu.querySelector(`[data-toggle="${menu.id.replace('-submenu', '')}"]`);
                                    if (otherParent) {
                                        otherParent.classList.remove('expanded');
                                        const otherChevron = otherParent.querySelector('.nav-chevron');
                                        if (otherChevron) {
                                            otherChevron.style.transform = '';
                                        }
                                    }
                                }
                            });
                        }
                    } else {
                        // Close all other top-level submenus
                        document.querySelectorAll('.nav-submenu.expanded').forEach(menu => {
                            if (menu !== submenu && !menu.classList.contains('nav-nested-submenu')) {
                                menu.classList.remove('expanded');
                                const otherParent = document.querySelector(`[data-toggle="${menu.id.replace('-submenu', '')}"]`);
                                if (otherParent && !otherParent.closest('.nav-nested')) {
                                    otherParent.classList.remove('expanded');
                                    const otherChevron = otherParent.querySelector('.nav-chevron');
                                    if (otherChevron) {
                                        otherChevron.style.transform = '';
                                    }
                                }
                            }
                        });
                    }
                    
                    // Toggle current submenu
                    if (isExpanded) {
                        submenu.classList.remove('expanded');
                        parent.classList.remove('expanded');
                        if (chevron) chevron.style.transform = '';
                    } else {
                        submenu.classList.add('expanded');
                        parent.classList.add('expanded');
                        if (chevron) chevron.style.transform = 'rotate(90deg)';
                    }
                }
            });
        });
    }
    
    // Function to close all expanded submenus
    function closeAllSubmenus() {
        document.querySelectorAll('.nav-submenu.expanded').forEach(menu => {
            menu.classList.remove('expanded');
            const parent = document.querySelector(`[data-toggle="${menu.id.replace('-submenu', '')}"]`);
            if (parent) {
                parent.classList.remove('expanded');
                const chevron = parent.querySelector('.nav-chevron');
                if (chevron) {
                    chevron.style.transform = '';
                }
            }
        });
    }
    
    // Initialize expandable navigation (after DOM is ready)
    setTimeout(() => {
        initExpandableNavigation();
    }, 100);

    // --- Drawer Management ---
    const overlay = document.getElementById('overlay');
    const selectionCart = document.getElementById('selectionCart');
    const aiAssistant = document.getElementById('aiAssistant');
    const cartToggle = document.getElementById('cartToggle');
    const assistantToggle = document.getElementById('assistantToggle');
    const cartClose = document.getElementById('cartClose');
    const assistantClose = document.getElementById('assistantClose');
    
    let isSidebarOpen = false;
    let isCartOpen = false;
    let isAssistantOpen = false;
    
    function updateOverlay() {
        const shouldShow = isSidebarOpen || isCartOpen || isAssistantOpen;
        overlay.style.display = shouldShow ? 'block' : 'none';
        overlay.setAttribute('aria-hidden', shouldShow ? 'false' : 'true');
    }
    
    function openCart() {
        isCartOpen = true;
        isAssistantOpen = false;
        selectionCart.setAttribute('aria-hidden', 'false');
        aiAssistant.setAttribute('aria-hidden', 'true');
        updateOverlay();
    }
    
    function closeCart() {
        isCartOpen = false;
        selectionCart.setAttribute('aria-hidden', 'true');
        updateOverlay();
    }
    
    function openAssistant() {
        isAssistantOpen = true;
        isCartOpen = false;
        aiAssistant.setAttribute('aria-hidden', 'false');
        selectionCart.setAttribute('aria-hidden', 'true');
        updateOverlay();
    }
    
    function closeAssistant() {
        isAssistantOpen = false;
        aiAssistant.setAttribute('aria-hidden', 'true');
        updateOverlay();
    }
    
    // Drawer event listeners
    cartToggle.addEventListener('click', () => {
        if (isCartOpen) closeCart(); else openCart();
    });
    
    assistantToggle.addEventListener('click', () => {
        if (isAssistantOpen) closeAssistant(); else openAssistant();
    });
    
    cartClose.addEventListener('click', closeCart);
    assistantClose.addEventListener('click', closeAssistant);

    menuBtn.addEventListener('click', () => {
        const isMobile = window.matchMedia('(max-width: 1024px)').matches;
        if (isMobile) {
            // Toggle mobile drawer
            isSidebarOpen = sidebar.classList.toggle('open');
            updateOverlay();
        } else {
            // Toggle desktop collapse
            const isCollapsing = !sidebar.classList.contains('collapsed');
            sidebar.classList.toggle('collapsed');
            
            // Close all submenus when collapsing
            if (isCollapsing) {
                closeAllSubmenus();
            }
        }
    });
    
    // Close drawers when clicking overlay
    overlay.addEventListener('click', () => {
        if (isSidebarOpen) {
            sidebar.classList.remove('open');
            isSidebarOpen = false;
        }
        if (isCartOpen) closeCart();
        if (isAssistantOpen) closeAssistant();
        updateOverlay();
    });
    
    // Close drawers with Escape key
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (isSidebarOpen) {
                sidebar.classList.remove('open');
                isSidebarOpen = false;
            }
            if (isCartOpen) closeCart();
            if (isAssistantOpen) closeAssistant();
            updateOverlay();
        }
    });
    

    // --- Router ---
    const routes = {
        '/': renderDashboard,
        '/dashboard': renderDashboard,
        '/packs': renderPacks,
        '/models': renderModels,
        '/models/new': renderModelCreate,
        '/models/:id/designer': renderModelDesigner,
        '/models/:id/composer': renderModelComposer,
        '/models/:id/composer/build': renderModelComposer,
        '/models/:id/composer/sweeps': renderModelComposer,
        '/models/:id/composer/leaderboard': renderModelComposer,
        '/models/:id/composer/backtest': renderModelComposer,
        '/models/:id/composer/train': renderModelComposer,
        '/signals': renderSignals,
        '/overlay': renderOverlay,
        '/health': renderHealth,
        '/docs': renderDocs,
        '/admin': renderAdmin,
    };

    const renderView = () => {
        const path = location.hash.replace(/^#/, '') || '/dashboard';
        const viewFn = routes[path] || routes['/dashboard']; // Default to dashboard
        app.innerHTML = '';
        app.appendChild(viewFn());

        // Set pack accent based on current page/context
        // For demo purposes, rotate through pack themes
        const packRotation = ['zerosigma', 'swingsigma', 'longsigma', 'overnightsigma', 'momentumsigma'];
        const currentPack = packRotation[Math.floor(Date.now() / 10000) % packRotation.length];
        root.setAttribute('data-edge', currentPack);

        // Update active nav link
        document.querySelectorAll('.nav-item').forEach(link => {
            link.classList.toggle('active', link.getAttribute('href') === `#${path}`);
        });
    };

    window.addEventListener('hashchange', renderView);
    renderView(); // Initial render
});
