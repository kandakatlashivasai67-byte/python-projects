/* ==========================================================================
   Feedback Ledger — client-side interactivity
   No frameworks: small, focused helpers per page.
   ========================================================================== */

/* ---- Toasts -------------------------------------------------------------- */
function showToast(message, type) {
  const stack = document.getElementById('toastStack');
  if (!stack) return;
  const toast = document.createElement('div');
  toast.className = 'toast' + (type === 'error' ? ' toast-error' : '');
  toast.textContent = message;
  stack.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('leaving');
    setTimeout(() => toast.remove(), 220);
  }, 3200);
}

document.addEventListener('DOMContentLoaded', function () {
  if (window.__flashMessages && window.__flashMessages.length) {
    window.__flashMessages.forEach(([category, message]) => {
      showToast(message, category === 'error' ? 'error' : 'success');
    });
  }
});

/* ---- Star rating caption --------------------------------------------------
   The stars themselves fill via pure CSS (see style.css) so the widget
   works even without JS. This layer only updates the human-readable
   caption next to the stars. */
function initStarRating(containerId, captionId) {
  const container = document.getElementById(containerId);
  const caption = document.getElementById(captionId);
  if (!container || !caption) return;

  const labels = {
    1: '1 — Needs real improvement',
    2: '2 — Below expectations',
    3: '3 — Satisfactory',
    4: '4 — Good',
    5: '5 — Excellent',
  };

  const inputs = container.querySelectorAll('input[type="radio"]');
  const setCaptionFromChecked = () => {
    const checked = container.querySelector('input[type="radio"]:checked');
    caption.textContent = checked ? labels[checked.value] : 'No rating yet';
  };

  inputs.forEach((input) => {
    input.addEventListener('change', setCaptionFromChecked);
    const label = container.querySelector(`label[for="${input.id}"]`);
    if (label) {
      label.addEventListener('mouseenter', () => {
        caption.textContent = labels[input.value];
      });
      label.addEventListener('mouseleave', setCaptionFromChecked);
    }
  });

  setCaptionFromChecked();
}

/* ---- Character counter ---------------------------------------------------- */
function initCharCounter(textareaId, counterId, max) {
  const textarea = document.getElementById(textareaId);
  const counter = document.getElementById(counterId);
  if (!textarea || !counter) return;

  const update = () => {
    const len = textarea.value.length;
    counter.textContent = `${len} / ${max}`;
    counter.classList.toggle('near-limit', len > max * 0.9);
  };
  textarea.addEventListener('input', update);
  update();
}

/* ---- Dashboard: animate distribution bars on load -------------------------- */
function initBarAnimation() {
  const bars = document.querySelectorAll('.bar-fill[data-pct]');
  requestAnimationFrame(() => {
    bars.forEach((bar) => {
      bar.style.width = bar.dataset.pct + '%';
    });
  });
}

/* ---- Dashboard: search, filter, sort, delete -------------------------------- */
function initDashboardTable() {
  const body = document.getElementById('ledgerBody');
  const table = document.getElementById('ledgerTable');
  if (!body || !table) return;

  const searchInput = document.getElementById('searchInput');
  const teacherFilter = document.getElementById('teacherFilter');
  const ratingFilter = document.getElementById('ratingFilter');
  const resultCount = document.getElementById('resultCount');
  const emptyState = document.getElementById('emptyState');

  function applyFilters() {
    const query = (searchInput.value || '').trim().toLowerCase();
    const teacher = teacherFilter.value;
    const rating = ratingFilter.value;
    let visible = 0;

    Array.from(body.querySelectorAll('tr')).forEach((row) => {
      const haystack = [
        row.dataset.student, row.dataset.roll, row.dataset.teacher,
        row.dataset.course, row.dataset.comment,
      ].join(' ').toLowerCase();

      const matchesQuery = !query || haystack.includes(query);
      const matchesTeacher = !teacher || row.dataset.teacher === teacher;
      const matchesRating = !rating || row.dataset.rating === rating;
      const show = matchesQuery && matchesTeacher && matchesRating;

      row.style.display = show ? '' : 'none';
      if (show) visible += 1;
    });

    resultCount.textContent = `${visible} of ${body.querySelectorAll('tr').length} entries`;
    emptyState.style.display = visible === 0 ? 'block' : 'none';
  }

  [searchInput, teacherFilter, ratingFilter].forEach((el) => {
    el.addEventListener('input', applyFilters);
    el.addEventListener('change', applyFilters);
  });
  applyFilters();

  /* Sorting */
  let sortState = { key: null, dir: 1 };
  table.querySelectorAll('th[data-sort]').forEach((th) => {
    th.addEventListener('click', () => {
      const key = th.dataset.sort;
      sortState.dir = sortState.key === key ? -sortState.dir : 1;
      sortState.key = key;

      const rows = Array.from(body.querySelectorAll('tr'));
      const dataKeyMap = { date: 'date', student: 'student', teacher: 'teacher', course: 'course', rating: 'rating' };
      const attr = dataKeyMap[key];

      rows.sort((a, b) => {
        let av = a.dataset[attr];
        let bv = b.dataset[attr];
        if (attr === 'rating') {
          av = Number(av); bv = Number(bv);
          return (av - bv) * sortState.dir;
        }
        return av.localeCompare(bv) * sortState.dir;
      });

      rows.forEach((row) => body.appendChild(row));

      table.querySelectorAll('th .arrow').forEach((a) => (a.textContent = '↕'));
      const arrow = th.querySelector('.arrow');
      if (arrow) arrow.textContent = sortState.dir === 1 ? '↑' : '↓';
    });
  });

  /* Delete with confirm modal */
  const modal = document.getElementById('confirmModal');
  const cancelBtn = document.getElementById('cancelDelete');
  const confirmBtn = document.getElementById('confirmDelete');
  let pendingRow = null;

  function openModal(row) {
    pendingRow = row;
    modal.classList.add('open');
  }
  function closeModal() {
    modal.classList.remove('open');
    pendingRow = null;
  }

  body.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-delete]');
    if (!btn) return;
    const row = btn.closest('tr');
    openModal(row);
  });

  if (cancelBtn) cancelBtn.addEventListener('click', closeModal);
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }

  if (confirmBtn) {
    confirmBtn.addEventListener('click', async () => {
      if (!pendingRow) return;
      const id = pendingRow.dataset.id;
      confirmBtn.disabled = true;
      confirmBtn.textContent = 'Deleting…';
      try {
        const res = await fetch(`/api/feedback/${id}`, { method: 'DELETE' });
        if (!res.ok) throw new Error('Request failed');
        pendingRow.style.transition = 'opacity 0.2s ease';
        pendingRow.style.opacity = '0';
        setTimeout(() => {
          pendingRow.remove();
          applyFilters();
          showToast('Entry deleted from the ledger.', 'success');
        }, 180);
      } catch (err) {
        showToast('Could not delete that entry. Try again.', 'error');
      } finally {
        confirmBtn.disabled = false;
        confirmBtn.textContent = 'Delete entry';
        closeModal();
      }
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });
}
