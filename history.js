// ============================================================================
// HISTORY CENTER - Fixed JavaScript Logic
// BUGFIX: Now shows ACTUAL previous questions & answers, not just summary
// ============================================================================

const state = {
    allHistory: [],
    filteredHistory: [],
    displayedHistory: [],
    currentView: 'grid',
    currentFilter: 'all',
    searchQuery: '',
    sortBy: 'recent',
    currentPage: 1,
    itemsPerPage: 12,
    selectedItem: null,
    selectedMessages: [], // ← NEW: Store messages for selected conversation
    deleteTarget: null
};

// ============================================================================
// DOM ELEMENTS
// ============================================================================

const elements = {
    searchInput: document.getElementById('searchInput'),
    filterTabs: document.querySelectorAll('.filter-tab'),
    historyGrid: document.getElementById('historyGrid'),
    historyList: document.getElementById('historyList'),
    emptyState: document.getElementById('emptyState'),
    loadingState: document.getElementById('loadingState'),
    sortSelect: document.getElementById('sortSelect'),
    gridViewBtn: document.getElementById('gridViewBtn'),
    listViewBtn: document.getElementById('listViewBtn'),
    detailModal: document.getElementById('detailModal'),
    modalCloseBtn: document.getElementById('modalCloseBtn'),
    modalTitle: document.getElementById('modalTitle'),
    modalSubtitle: document.getElementById('modalSubtitle'),
    modalIcon: document.getElementById('modalIcon'),
    modalBody: document.getElementById('modalBody'),
    toast: document.getElementById('toast'),
    countAll: document.getElementById('countAll'),
    countUrl: document.getElementById('countUrl'),
    countDocument: document.getElementById('countDocument')
};

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    loadHistory();
    setupEventListeners();
}

function setupEventListeners() {
    // Search
    elements.searchInput.addEventListener('input', handleSearch);
    
    // Filter tabs
    elements.filterTabs.forEach(tab => {
        tab.addEventListener('click', handleFilterChange);
    });
    
    // Sort
    elements.sortSelect.addEventListener('change', handleSort);
    
    // View toggle
    elements.gridViewBtn.addEventListener('click', () => setView('grid'));
    elements.listViewBtn.addEventListener('click', () => setView('list'));
    
    // Modal
    elements.modalCloseBtn.addEventListener('click', closeDetailModal);
    elements.detailModal.addEventListener('click', (e) => {
        if (e.target === elements.detailModal) closeDetailModal();
    });
}

// ============================================================================
// DATA LOADING - FETCH FROM BACKEND API
// ============================================================================

async function loadHistory() {
    elements.loadingState.style.display = 'block';
    try {
        // FIXED: Uncommented the actual API call!
        const res = await fetch('/api/history');
        
        if (!res.ok) {
            throw new Error('Failed to load history');
        }
        
        const data = await res.json();
        
        if (data.success) {
            // Map backend data to frontend format
            state.allHistory = (data.items || []).map(item => ({
                conversation_id: item.conversation_id,
                user_id: item.user_id,
                title: item.title || 'Untitled Conversation',
                conversation_type: item.conversation_type, // 'URL' or 'DOCUMENT'
                created_at: new Date(item.created_at),
                updated_at: new Date(item.updated_at),
                executive_summary: item.executive_summary || 'No summary available',
                message_count: item.message_count || 0,
                sentiment: item.sentiment || null,
                source_type: item.source_type,
                source_url: item.source_url,
                file_name: item.file_name,
                // These will be loaded separately
                messages: []
            }));
            
            updateCounts();
            filterAndRender();
        } else {
            elements.emptyState.style.display = 'block';
        }
    } catch (err) {
        console.error('Error loading history:', err);
        elements.loadingState.innerHTML = '<p>Error loading history. Please refresh the page.</p>';
        showToast('Failed to load history', 'error');
    } finally {
        elements.loadingState.style.display = 'none';
    }
}

// ============================================================================
// FETCH MESSAGES FOR CONVERSATION
// ============================================================================

async function fetchConversationMessages(conversationId) {
    try {
        const res = await fetch(`/api/conversations/${conversationId}/messages`);
        
        if (!res.ok) {
            console.error('Failed to fetch messages');
            return [];
        }
        
        const data = await res.json();
        return data.messages || [];
    } catch (err) {
        console.error('Error fetching messages:', err);
        return [];
    }
}

// ============================================================================
// SEARCH & FILTER
// ============================================================================

function handleSearch(e) {
    state.searchQuery = e.target.value.toLowerCase().trim();
    state.currentPage = 1;
    filterAndRender();
}

function handleFilterChange(e) {
    const filter = e.currentTarget.dataset.filter;
    state.currentFilter = filter;
    state.currentPage = 1;
    
    elements.filterTabs.forEach(tab => {
        tab.classList.remove('active');
    });
    e.currentTarget.classList.add('active');
    
    filterAndRender();
}

function filterAndRender() {
    let filtered = [...state.allHistory];
    
    if (state.currentFilter !== 'all') {
        filtered = filtered.filter(item => item.conversation_type === state.currentFilter);
    }
    
    if (state.searchQuery) {
        filtered = filtered.filter(item => {
            const searchableText = `${item.title} ${item.executive_summary || ''}`.toLowerCase();
            return searchableText.includes(state.searchQuery);
        });
    }
    
    state.filteredHistory = filtered;
    applySort();
    render();
}

// ============================================================================
// SORTING
// ============================================================================

function handleSort(e) {
    state.sortBy = e.target.value;
    applySort();
    render();
}

function applySort() {
    const sorted = [...state.filteredHistory];
    
    switch (state.sortBy) {
        case 'recent':
            sorted.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
            break;
        case 'oldest':
            sorted.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
            break;
        case 'type':
            sorted.sort((a, b) => a.conversation_type.localeCompare(b.conversation_type));
            break;
    }
    
    state.filteredHistory = sorted;
}

// ============================================================================
// VIEW MANAGEMENT
// ============================================================================

function setView(view) {
    state.currentView = view;
    
    if (view === 'grid') {
        elements.gridViewBtn.classList.add('active');
        elements.listViewBtn.classList.remove('active');
        elements.historyGrid.style.display = 'grid';
        elements.historyList.style.display = 'none';
    } else {
        elements.gridViewBtn.classList.remove('active');
        elements.listViewBtn.classList.add('active');
        elements.historyGrid.style.display = 'none';
        elements.historyList.style.display = 'flex';
    }
    
    render();
}

// ============================================================================
// RENDERING
// ============================================================================

function updateCounts() {
    elements.countAll.textContent = state.allHistory.length;
    elements.countUrl.textContent = state.allHistory.filter(i => i.conversation_type === 'URL').length;
    elements.countDocument.textContent = state.allHistory.filter(i => i.conversation_type === 'DOCUMENT').length;
}

function render() {
    const total = state.filteredHistory.length;
    
    if (total === 0) {
        elements.emptyState.style.display = 'block';
        elements.historyGrid.innerHTML = '';
        elements.historyList.innerHTML = '';
        return;
    }
    
    elements.emptyState.style.display = 'none';
    
    if (state.currentView === 'grid') {
        renderGrid();
    } else {
        renderList();
    }
}

function renderGrid() {
    elements.historyGrid.innerHTML = state.filteredHistory.map(item => `
        <article class="history-card" data-id="${item.conversation_id}">
            <div class="history-badge">
                ${item.conversation_type === 'URL' ? '🔗 Video' : '📄 Document'}
            </div>
            <div class="history-meta">
                <span>${item.conversation_type === 'URL' ? 'YouTube' : 'Document'}</span>
                <span>${formatDate(item.updated_at)}</span>
            </div>
            <h3 class="history-title">${escapeHtml(item.title)}</h3>
            <div class="history-snippet">${escapeHtml((item.executive_summary || 'No summary').slice(0, 200))}</div>
        </article>
    `).join('');
    
    attachCardListeners();
}

function renderList() {
    elements.historyList.innerHTML = state.filteredHistory.map(item => `
        <article class="history-card" data-id="${item.conversation_id}">
            <div class="history-badge">
                ${item.conversation_type === 'URL' ? '🔗 Video' : '📄 Document'}
            </div>
            <div class="history-meta">
                <span>${item.conversation_type === 'URL' ? 'YouTube' : 'Document'}</span>
                <span>${formatDate(item.updated_at)}</span>
            </div>
            <h3 class="history-title">${escapeHtml(item.title)}</h3>
            <div class="history-snippet">${escapeHtml((item.executive_summary || 'No summary').slice(0, 200))}</div>
        </article>
    `).join('');
    
    attachCardListeners();
}

function attachCardListeners() {
    document.querySelectorAll('.history-card').forEach(card => {
        card.addEventListener('click', async () => {
            const conversationId = card.dataset.id;
            const item = state.allHistory.find(i => i.conversation_id == conversationId);
            if (item) {
                await openDetailModal(item);
            }
        });
    });
}

// ============================================================================
// MODAL - FIXED: NOW SHOWS ACTUAL MESSAGES!
// ============================================================================

async function openDetailModal(item) {
    state.selectedItem = item;
    
    // Set header info
    elements.modalTitle.textContent = item.title || 'Untitled';
    elements.modalSubtitle.textContent = `${item.conversation_type === 'URL' ? '🔗 Video' : '📄 Document'} • ${formatDate(item.updated_at)}`;
    elements.modalIcon.innerHTML = item.conversation_type === 'DOCUMENT' ? '📄' : '🔗';
    
    // Show loading state while fetching messages
    elements.modalBody.innerHTML = '<div style="padding: 20px; text-align: center; color: rgba(255,255,255,0.7);">Loading conversation...</div>';
    elements.detailModal.style.display = 'flex';
    
    // FIXED: Fetch actual messages from database!
    const messages = await fetchConversationMessages(item.conversation_id);
    state.selectedMessages = messages;
    
    // Build modal content with messages
    let modalContent = '';
    
    // Show summary section
    modalContent += `
        <div class="detail-block">
            <div class="detail-label">Summary</div>
            <div class="detail-value">${escapeHtml(item.executive_summary || 'No summary available.')}</div>
        </div>
    `;
    
    // Show sentiment if available
    if (item.sentiment) {
        modalContent += `
            <div class="detail-block">
                <div class="detail-label">Sentiment</div>
                <div class="detail-value">${escapeHtml(item.sentiment)}</div>
            </div>
        `;
    }
    
    // FIXED: Show ACTUAL CONVERSATION MESSAGES! ← THIS WAS MISSING!
    if (messages.length > 0) {
        modalContent += `
            <div class="detail-block">
                <div class="detail-label">Conversation History</div>
                <div class="detail-value" style="display: flex; flex-direction: column; gap: 12px; max-height: 400px; overflow-y: auto;">
        `;
        
        messages.forEach(msg => {
            const isUser = msg.role === 'user';
            const bgColor = isUser ? 'rgba(0, 191, 255, 0.15)' : 'rgba(255, 255, 255, 0.05)';
            const label = isUser ? 'You' : 'AI Assistant';
            
            modalContent += `
                <div style="background: ${bgColor}; padding: 12px; border-radius: 8px; border-left: 3px solid ${isUser ? '#00bfff' : 'rgba(255,255,255,0.3)'};">
                    <div style="font-size: 12px; font-weight: 600; color: rgba(255,255,255,0.8); margin-bottom: 6px;">${label}</div>
                    <div style="color: rgba(255,255,255,0.9); line-height: 1.6; word-wrap: break-word;">
                        ${escapeHtml(msg.content)}
                    </div>
                    <div style="font-size: 11px; color: rgba(255,255,255,0.5); margin-top: 6px;">
                        ${formatDate(new Date(msg.created_at))}
                    </div>
                </div>
            `;
        });
        
        modalContent += `
                </div>
            </div>
        `;
    } else {
        modalContent += `
            <div class="detail-block">
                <div class="detail-label">Conversation</div>
                <div class="detail-value">No messages yet. Start a conversation to see Q&A history.</div>
            </div>
        `;
    }
    
    // Show stats
    modalContent += `
        <div class="detail-block">
            <div class="detail-label">Total Messages</div>
            <div class="detail-value">${item.message_count || messages.length} messages</div>
        </div>
    `;
    
    // Action buttons
    modalContent += `
        <div style="display: flex; gap: 12px; margin-top: 20px;">
            <button id="continueBtn" class="btn-primary" style="flex: 1; padding: 12px; border-radius: 12px; background: #00bfff; color: #fff; border: none; cursor: pointer; font-weight: 700;">Continue Conversation</button>
            <button id="closeBtn" class="btn-secondary" style="flex: 1; padding: 12px; border-radius: 12px; background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); cursor: pointer; font-weight: 700;">Close</button>
        </div>
    `;
    
    elements.modalBody.innerHTML = modalContent;
    
    // Add event listeners
    document.getElementById('continueBtn').addEventListener('click', () => {
        window.location.href = `/chat?id=${item.conversation_id}`;
    });
    
    document.getElementById('closeBtn').addEventListener('click', closeDetailModal);
}

function closeDetailModal() {
    elements.detailModal.style.display = 'none';
    state.selectedItem = null;
    state.selectedMessages = [];
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function formatDate(dateStr) {
    try {
        const date = typeof dateStr === 'string' ? new Date(dateStr) : dateStr;
        if (Number.isNaN(date.getTime())) return 'Unknown date';
        
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (e) {
        return String(dateStr);
    }
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showToast(message, type = 'success') {
    elements.toast.textContent = message;
    elements.toast.style.display = 'block';
    setTimeout(() => {
        elements.toast.style.display = 'none';
    }, 3000);
}