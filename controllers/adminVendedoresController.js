var API_URL = "/api";

function getToken() {
    return localStorage.getItem("access_token");
}

var PAISES = [
    { codigo: 'AR', nombre: 'Argentina' }, { codigo: 'BO', nombre: 'Bolivia' },
    { codigo: 'BR', nombre: 'Brasil' }, { codigo: 'CL', nombre: 'Chile' },
    { codigo: 'CO', nombre: 'Colombia' }, { codigo: 'CR', nombre: 'Costa Rica' },
    { codigo: 'DO', nombre: 'República Dominicana' }, { codigo: 'EC', nombre: 'Ecuador' },
    { codigo: 'GT', nombre: 'Guatemala' }, { codigo: 'MX', nombre: 'México' },
    { codigo: 'NI', nombre: 'Nicaragua' }, { codigo: 'PA', nombre: 'Panamá' },
    { codigo: 'PE', nombre: 'Perú' }, { codigo: 'PY', nombre: 'Paraguay' },
    { codigo: 'SV', nombre: 'El Salvador' }, { codigo: 'UY', nombre: 'Uruguay' },
    { codigo: 'VE', nombre: 'Venezuela' }
];

let vendedoresPlanes = [];

async function cargarPlanesVendedores() {
    try {
        const res = await fetch(`${API_URL}/plans`);
        if (res.ok) {
            const data = await res.json();
            vendedoresPlanes = data.planes;
        }
    } catch {
        vendedoresPlanes = [];
    }
}

function getPlanName(id) {
    const p = vendedoresPlanes.find(x => x.id === id);
    return p ? p.nombre_plan : 'Desconocido';
}

function getPaisName(code) {
    const p = PAISES.find(x => x.codigo === code);
    return p ? p.nombre : code;
}

function getBadgeClass(planId) {
    if (planId === 3) return 'badge-green';
    if (planId === 2) return 'badge-yellow';
    return 'badge-red';
}

let currentPage = 1;
let totalPages = 1;
let vendedoresData = [];
let searchTerm = '';
let planesLoaded = false;

async function ensurePlanesLoaded() {
    if (!planesLoaded) {
        await cargarPlanesVendedores();
        planesLoaded = true;
    }
}

async function renderVendedoresSection() {
    await ensurePlanesLoaded();
    const container = document.getElementById('section-vendedores');
    if (!container) return;

    container.innerHTML = `
        <div class="crud-header">
            <h2>Gestión de Vendedores</h2>
            <div class="crud-toolbar">
                <input id="search-vendedores" class="search-bar" type="text" placeholder="Buscar vendedor..." value="${searchTerm}">
            </div>
        </div>
        <div class="section-card">
            <div class="admin-table-wrap">
                <table class="dime-table">
                    <thead>
                        <tr>
                            <th style="padding:10px 12px;width:50px">ID</th>
                            <th style="padding:10px 12px">Usuario</th>
                            <th style="padding:10px 12px">Tienda</th>
                            <th style="padding:10px 12px">Email</th>
                            <th style="padding:10px 12px">País</th>
                            <th style="padding:10px 12px">Plan</th>
                            <th style="padding:10px 12px;text-align:center">Estado</th>
                            <th style="padding:10px 12px;text-align:center;width:140px">Acciones</th>
                        </tr>
                    </thead>
                    <tbody id="vendedores-tbody">
                        <tr>
                            <td colspan="8" style="text-align:center;padding:32px;color:var(--text-muted)">Cargando...</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div id="vendedores-pagination" style="display:flex;align-items:center;justify-content:center;gap:8px;padding:12px 0;margin-top:8px"></div>
        </div>
    `;

    document.getElementById('search-vendedores').addEventListener('input', function () {
        searchTerm = this.value;
        currentPage = 1;
        fetchVendedores();
    });

    await fetchVendedores();
}

async function fetchVendedores() {
    const tbody = document.getElementById('vendedores-tbody');
    const pagination = document.getElementById('vendedores-pagination');
    if (!tbody) return;

    try {
        const token = getToken();
        const params = new URLSearchParams({ page: currentPage, per_page: '10' });
        if (searchTerm) params.set('search', searchTerm);

        const res = await fetch(`${API_URL}/admin/vendedores?${params}`, {
            headers: {
                Authorization: token ? `Bearer ${token}` : '',
            },
        });

        if (!res.ok) {
            if (res.status === 403) {
                tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;padding:32px;color:var(--danger)">Acceso denegado. Solo administradores.</td></tr>`;
            } else {
                tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;padding:32px;color:var(--danger)">Error al cargar vendedores (${res.status})</td></tr>`;
            }
            if (pagination) pagination.innerHTML = '';
            return;
        }

        const data = await res.json();
        vendedoresData = data.vendedores || [];
        totalPages = data.total_pages || 1;

        if (!vendedoresData.length) {
            tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;padding:32px;color:var(--text-muted)">Sin resultados</td></tr>`;
        } else {
            tbody.innerHTML = vendedoresData.map(v => {
                const badgeClass = getBadgeClass(v.tipo_plan);
                const statusClass = v.esta_activo ? 'badge-active' : 'badge-inactive';
                const statusText = v.esta_activo ? 'Activo' : 'Inactivo';
                return `
                    <tr>
                        <td style="padding:10px 12px;font-family:'JetBrains Mono',monospace;font-size:11px">${v.id_vendedor}</td>
                        <td style="padding:10px 12px;font-weight:600;color:var(--primary)">${v.user_name}</td>
                        <td style="padding:10px 12px">${v.nombre_tienda}</td>
                        <td style="padding:10px 12px;font-size:11px">${v.email}</td>
                        <td style="padding:10px 12px;font-size:11px">${getPaisName(v.codigo_pais)}</td>
                        <td style="padding:10px 12px"><span class="badge ${badgeClass}" style="font-size:10px">${getPlanName(v.tipo_plan)}</span></td>
                        <td style="padding:10px 12px;text-align:center"><span class="badge-status ${statusClass}">${statusText}</span></td>
                        <td style="padding:10px 12px;text-align:center">
                            <div class="table-actions">
                                <button class="btn-edit" onclick="toggleVendedorStatus(${v.id_vendedor})">${v.esta_activo ? 'Desactivar' : 'Activar'}</button>
                                <button class="btn-delete" onclick="openDeleteVendedor(${v.id_vendedor}, '${v.user_name.replace(/'/g, "\\'")}')">Eliminar</button>
                            </div>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        if (pagination) renderPagination(pagination, data);

    } catch (error) {
        console.error('Error fetching vendedores:', error);
        tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;padding:32px;color:var(--danger)">Error de conexión</td></tr>`;
        if (pagination) pagination.innerHTML = '';
    }
}

function renderPagination(container, data) {
    const page = data.page || currentPage;
    const pages = data.total_pages || totalPages;

    if (pages <= 1) {
        container.style.display = 'none';
        return;
    }
    container.style.display = 'flex';

    let html = '';
    html += `<button class="btn-edit" onclick="goToPage(${page - 1})" ${page <= 1 ? 'disabled style="opacity:0.4;cursor:not-allowed"' : ''}>Anterior</button>`;

    let start = Math.max(1, page - 2);
    let end = Math.min(pages, page + 2);

    if (start > 1) {
        html += `<button class="btn-edit" onclick="goToPage(1)">1</button>`;
        if (start > 2) html += `<span style="color:var(--text-muted);font-size:11px">...</span>`;
    }

    for (let i = start; i <= end; i++) {
        html += `<button class="btn-edit${i === page ? ' active-page' : ''}" onclick="goToPage(${i})">${i}</button>`;
    }

    if (end < pages) {
        if (end < pages - 1) html += `<span style="color:var(--text-muted);font-size:11px">...</span>`;
        html += `<button class="btn-edit" onclick="goToPage(${pages})">${pages}</button>`;
    }

    html += `<button class="btn-edit" onclick="goToPage(${page + 1})" ${page >= pages ? 'disabled style="opacity:0.4;cursor:not-allowed"' : ''}>Siguiente</button>`;

    html += `<span style="font-size:11px;color:var(--text-muted);font-family:'JetBrains Mono',monospace;margin-left:8px">Pág ${page} de ${pages}</span>`;

    container.innerHTML = html;
}

window.goToPage = function (page) {
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    fetchVendedores();
};

window.toggleVendedorStatus = async function (vendedorId) {
    try {
        const token = getToken();
        const res = await fetch(`${API_URL}/admin/vendedores/${vendedorId}/toggle-status`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                Authorization: token ? `Bearer ${token}` : '',
            },
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            showToast(err.detail || 'Error al cambiar estado', 'error');
            return;
        }

        showToast('Estado actualizado correctamente', 'success');
        await fetchVendedores();
    } catch {
        showToast('Error de conexión con el servidor', 'error');
    }
};

window.openDeleteVendedor = function (vendedorId, userName) {
    const deleteMsg = document.getElementById('delete-msg');
    const confirmBtn = document.getElementById('btn-confirm-delete');
    if (deleteMsg) {
        deleteMsg.textContent = `¿Estás seguro de eliminar al vendedor "${userName}"? Esta acción no se puede deshacer.`;
    }
    if (confirmBtn) {
        confirmBtn.onclick = async function () {
            try {
                const token = getToken();
                const res = await fetch(`${API_URL}/admin/vendedores/${vendedorId}`, {
                    method: 'DELETE',
                    headers: {
                        Authorization: token ? `Bearer ${token}` : '',
                    },
                });

                if (!res.ok && res.status !== 204) {
                    const err = await res.json().catch(() => ({}));
                    showToast(err.detail || 'Error al eliminar vendedor', 'error');
                    return;
                }

                showToast('Vendedor eliminado correctamente', 'success');
                closeDeleteModal();
                await fetchVendedores();
            } catch {
                showToast('Error de conexión con el servidor', 'error');
                closeDeleteModal();
            }
        };
    }
    const deleteModal = document.getElementById('delete-modal');
    if (deleteModal) deleteModal.style.display = 'flex';
};

function showToast(msg, type) {
    const el = document.createElement('div');
    el.className = 'toast toast-' + type;
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(() => {
        el.style.opacity = '0';
        el.style.transition = 'opacity 0.3s';
        setTimeout(() => el.remove(), 300);
    }, 2500);
}

function closeDeleteModal() {
    const deleteModal = document.getElementById('delete-modal');
    if (deleteModal) deleteModal.style.display = 'none';
    const confirmBtn = document.getElementById('btn-confirm-delete');
    if (confirmBtn) confirmBtn.onclick = null;
}

window.renderAdminVendedores = renderVendedoresSection;
