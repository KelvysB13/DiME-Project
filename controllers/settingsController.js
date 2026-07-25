const API_URL = "/api";

function getToken() {
    return localStorage.getItem("access_token");
}

document.addEventListener("DOMContentLoaded", () => {
    // Theme toggle
    var themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', function() {
        var current = document.documentElement.getAttribute('data-theme');
        var next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
      });
    }
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
      if (!localStorage.getItem('theme')) {
        document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
      }
    });

    const navButtons = document.querySelectorAll(".sidebar nav .nav-btn");
    const views = document.querySelectorAll(".content-view");

    navButtons.forEach((btn) => {
        btn.addEventListener("click", function () {
            navButtons.forEach((b) => b.classList.remove("active"));
            this.classList.add("active");

            views.forEach((v) => v.classList.remove("active"));
            const targetView = this.getAttribute("data-view");
            document.getElementById(targetView).classList.add("active");
        });
    });

    cargarInformacionGeneral();
    cargarPlan();

    const btnShowForm = document.getElementById("btn-show-form");
    const formTarjeta = document.getElementById("form-nueva-tarjeta");
    const btnCancelCard = document.getElementById("btn-cancel-card");
    const btnSaveCard = document.getElementById("btn-save-card");

    btnShowForm.addEventListener("click", () => {
        btnShowForm.style.display = "none";
        formTarjeta.style.display = "block";
    });

    btnCancelCard.addEventListener("click", () => {
        formTarjeta.style.display = "none";
        btnShowForm.style.display = "block";
    });

    btnSaveCard.addEventListener("click", async () => {
        const titular = document.getElementById("titular_tarjeta").value.trim();
        const numero = document.getElementById("num_tarjeta").value.trim();
        const mes = parseInt(document.getElementById("mes_tarjeta").value, 10);
        const anio = parseInt(document.getElementById("anio_tarjeta").value, 10);
        const cvv = document.getElementById("cvv_tarjeta").value.trim();

        if (!titular || numero.length < 15 || !mes || !anio || !cvv) {
            alert("Por favor, completa todos los campos correctamente.");
            return;
        }

        const payload = {
            nombre_titular: titular,
            numero_tarjeta: numero,
            mes_caducidad: mes,
            anio_caducidad: anio,
            cvv: cvv,
        };

        try {
            const token = getToken();
            btnSaveCard.innerText = "Guardando...";
            btnSaveCard.style.pointerEvents = "none";

            const response = await fetch(`${API_URL}/payment/method`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: token ? `Bearer ${token}` : "",
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);

            alert("Método de pago agregado exitosamente.");
            document.getElementById("titular_tarjeta").value = "";
            document.getElementById("num_tarjeta").value = "";
            document.getElementById("mes_tarjeta").value = "";
            document.getElementById("anio_tarjeta").value = "";
            document.getElementById("cvv_tarjeta").value = "";

            formTarjeta.style.display = "none";
            btnShowForm.style.display = "block";
        } catch (error) {
            console.error("Fallo al guardar tarjeta:", error);
            alert("Hubo un problema al guardar la tarjeta. Verifica los datos.");
        } finally {
            btnSaveCard.innerText = "Guardar Tarjeta";
            btnSaveCard.style.pointerEvents = "auto";
        }
    });

    const btnUpdatePassword = document.getElementById("btn-update-password");

    btnUpdatePassword.addEventListener("click", async () => {
        const currentPassword = document.getElementById("current_password").value;
        const newPassword = document.getElementById("new_password").value;
        const confirmPassword = document.getElementById("confirm_new_password").value;

        if (!currentPassword || !newPassword || !confirmPassword) {
            alert("Por favor, completa todos los campos de contraseña.");
            return;
        }

        if (newPassword !== confirmPassword) {
            alert("La nueva contraseña y la confirmación no coinciden.");
            return;
        }

        const payload = {
            current_password: currentPassword,
            new_password: newPassword,
            confirm_new_password: confirmPassword,
        };

        try {
            const token = getToken();
            btnUpdatePassword.innerText = "Actualizando...";
            btnUpdatePassword.style.pointerEvents = "none";

            const response = await fetch(`${API_URL}/update-password`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: token ? `Bearer ${token}` : "",
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);

            alert("Contraseña actualizada exitosamente.");
            document.getElementById("current_password").value = "";
            document.getElementById("new_password").value = "";
            document.getElementById("confirm_new_password").value = "";
        } catch (error) {
            console.error("Fallo al actualizar contraseña:", error);
            alert("Error al actualizar la contraseña. Verifica que tu contraseña actual sea correcta.");
        } finally {
            btnUpdatePassword.innerText = "Actualizar Contraseña";
            btnUpdatePassword.style.pointerEvents = "auto";
        }
    });

    const btnDeleteAccount = document.getElementById("btn-delete-account");

    btnDeleteAccount.addEventListener("click", async () => {
        const confirmar = window.confirm(
            "¿Estás seguro que deseas eliminar tu cuenta? Esta acción no se puede deshacer."
        );

        if (confirmar) {
            try {
                const token = getToken();
                const response = await fetch(`${API_URL}/account-deletion`, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: token ? `Bearer ${token}` : "",
                    },
                });

                if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);

                alert("Tu cuenta ha sido eliminada con éxito.");
                localStorage.removeItem("access_token");
                window.location.href = "/";
            } catch (error) {
                console.error("Fallo al eliminar la cuenta:", error);
                alert("Hubo un problema al intentar eliminar la cuenta.");
            }
        }
    });
});

async function cargarInformacionGeneral() {
    try {
        const token = getToken();
        const response = await fetch(`${API_URL}/general-information`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: token ? `Bearer ${token}` : "",
            },
        });

        if (!response.ok) throw new Error(`Error del servidor: ${response.status}`);

        const data = await response.json();

        document.getElementById("username").value = data.user_name || "No definido";
        document.getElementById("nombre_tienda").value = data.nombre_tienda || "No definido";
        document.getElementById("email").value = data.email || "No definido";
        document.getElementById("pais").value = data.nombre_pais || "No definido";
    } catch (error) {
        console.error("Fallo al cargar la información general:", error);
    }
}

let allPlanes = [];
let currentPlanId = null;

async function cargarPlan() {
    try {
        const token = getToken();

        const [resPlan, resPersonal] = await Promise.all([
            fetch(`${API_URL}/plans`),
            fetch(`${API_URL}/personal-data`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: token ? `Bearer ${token}` : "",
                },
            }),
        ]);

        if (resPersonal.ok && resPlan.ok) {
            const data = await resPersonal.json();
            const { planes } = await resPlan.json();

            allPlanes = planes;
            currentPlanId = data.tipo_plan;

            const planActual = planes.find((p) => p.id === data.tipo_plan);

            document.getElementById("nombre_del_plan").innerText = planActual
                ? planActual.nombre_plan
                : "Plan Desconocido";
            document.getElementById("precio_del_plan").innerText = planActual
                ? "$" + planActual.precio_mensual.toFixed(2) + " USD"
                : "--";

            injectCambiarPlanBtn();
        }
    } catch (error) {
        console.error("Fallo al cargar el plan:", error);
        document.getElementById("nombre_del_plan").innerText = "Error al cargar";
    }
}

function injectCambiarPlanBtn() {
    const existing = document.getElementById("btn-cambiar-plan");
    if (existing) existing.remove();

    const renameP = document.querySelector("#view-billing .section-card p.text-xs");
    if (!renameP) return;

    const btn = document.createElement("button");
    btn.id = "btn-cambiar-plan";
    btn.className = "btn-retry";
    btn.style.marginTop = "12px";
    btn.style.width = "100%";
    btn.textContent = "Cambiar Plan";
    btn.addEventListener("click", abrirModalPlanes);
    renameP.parentNode.insertBefore(btn, renameP.nextSibling);
}

function abrirModalPlanes() {
    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";
    overlay.id = "modal-cambiar-plan";
    overlay.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,0.4);display:flex;align-items:center;justify-content:center;z-index:100;padding:20px";

    const box = document.createElement("div");
    box.style.cssText = "background:#fff;border-radius:12px;width:100%;max-width:480px;max-height:85vh;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,0.2);animation:fadeIn 0.15s ease-out";

    box.innerHTML = `
        <div style="display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid var(--border-light)">
            <h3 style="font-size:15px;font-weight:700;color:var(--primary)">Seleccionar Plan</h3>
            <button id="btn-cerrar-modal-plan" style="width:28px;height:28px;border-radius:50%;border:none;background:none;cursor:pointer;font-size:16px;color:var(--text-muted);display:flex;align-items:center;justify-content:center">✕</button>
        </div>
        <div style="padding:20px;overflow-y:auto;flex:1" id="modal-plan-body">
            ${allPlanes.map(p => `
                <label class="plan-option-modal" style="display:flex;align-items:center;gap:12px;padding:12px 16px;border:2px solid ${p.id === currentPlanId ? "var(--primary)" : "var(--border-light)"};border-radius:var(--radius-md);margin-bottom:8px;cursor:pointer;transition:border-color 0.15s;background-color:${p.id === currentPlanId ? "rgba(3,28,60,0.03)" : "transparent"}">
                    <input type="radio" name="plan-selection-modal" value="${p.id}" ${p.id === currentPlanId ? "checked" : ""} style="accent-color:var(--primary)">
                    <div style="flex:1">
                        <strong style="font-size:14px;color:var(--primary)">${p.nombre_plan}</strong>
                        <p style="font-size:11px;color:var(--text-muted);margin-top:2px">${p.descripcion || ""}</p>
                    </div>
                    <div style="text-align:right">
                        <span style="font-size:16px;font-weight:700">${p.precio_mensual === 0 ? "Gratis" : "$" + p.precio_mensual.toFixed(2)}</span>
                        ${p.precio_mensual > 0 ? '<span style="font-size:11px;color:var(--text-muted)">/mes</span>' : ""}
                    </div>
                </label>
            `).join("")}
        </div>
        <div style="display:flex;justify-content:flex-end;gap:8px;padding:14px 20px;border-top:1px solid var(--border-light)">
            <button id="btn-cancelar-plan-modal" style="padding:8px 16px;border-radius:6px;border:1px solid var(--border);background:none;font-size:12px;font-weight:600;cursor:pointer;color:var(--text-secondary);font-family:'Inter',sans-serif">Cancelar</button>
            <button id="btn-confirmar-plan-modal" style="padding:8px 16px;border-radius:6px;border:none;background-color:var(--primary);color:#fff;font-size:12px;font-weight:600;cursor:pointer;font-family:'Inter',sans-serif">Confirmar Cambio</button>
        </div>
    `;

    overlay.appendChild(box);
    document.body.appendChild(overlay);

    overlay.querySelectorAll(".plan-option-modal").forEach(label => {
        label.addEventListener("click", function () {
            overlay.querySelectorAll(".plan-option-modal").forEach(l => {
                l.style.borderColor = "var(--border-light)";
                l.style.backgroundColor = "transparent";
            });
            this.style.borderColor = "var(--primary)";
            this.style.backgroundColor = "rgba(3,28,60,0.03)";
            this.querySelector("input[type=radio]").checked = true;
        });
    });

    document.getElementById("btn-cerrar-modal-plan").onclick = () => overlay.remove();
    document.getElementById("btn-cancelar-plan-modal").onclick = () => overlay.remove();
    document.getElementById("btn-confirmar-plan-modal").onclick = async () => {
        const selected = overlay.querySelector('input[name="plan-selection-modal"]:checked');
        if (!selected) return;

        const newPlanId = parseInt(selected.value, 10);
        if (newPlanId === currentPlanId) {
            alert("Ya estás en este plan.");
            overlay.remove();
            return;
        }

        const planName = allPlanes.find(p => p.id === newPlanId)?.nombre_plan || "Desconocido";
        if (!window.confirm(`¿Estás seguro de cambiar al plan "${planName}"?`)) return;

        const btnConfirm = document.getElementById("btn-confirmar-plan-modal");
        btnConfirm.textContent = "Cambiando...";
        btnConfirm.style.pointerEvents = "none";

        try {
            const token = getToken();
            const res = await fetch(`${API_URL}/vendedor/plan`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: token ? `Bearer ${token}` : "",
                },
                body: JSON.stringify({ tipo_plan: newPlanId }),
            });

            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err.detail || `Error HTTP: ${res.status}`);
            }

            alert("Plan actualizado exitosamente.");
            overlay.remove();
            currentPlanId = newPlanId;
            await cargarPlan();
        } catch (error) {
            console.error("Fallo al cambiar de plan:", error);
            alert("Hubo un problema al cambiar de plan. Intenta de nuevo.");
        }
    };

    overlay.addEventListener("click", e => {
        if (e.target === overlay) overlay.remove();
    });
}
