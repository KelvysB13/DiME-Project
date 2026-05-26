# DiME - Diagrama Entidad-Relación

## Base Maestra: `dime_maestra`

```
┌─────────────────────────────┐
│         clientes            │
├─────────────────────────────┤
│ PK │ id_cliente          INT│
│    │ nombre_organizacion  VC│
│    │ email               VC│
│    │ plan                VC│
│    │ fecha_registro   DATE│
│    │ db_name             VC│
└─────────────────────────────┘

┌─────────────────────────────┐
│    servicios_ofrecidos      │
├─────────────────────────────┤
│ PK │ id_servicio         INT│
│    │ nombre_servicio     VC│
│    │ descripcion        TXT│
│    │ precio_referencia DEC│
│    │ area_asociada      VC│
└─────────────────────────────┘
```

## Base por Cliente: `dime_cliente_X`

```
┌─────────────────────────────────┐
│    metricas_publicaciones       │
├─────────────────────────────────┤
│ PK │ id_publicacion          INT│
│    │ titulo                  VC│
│    │ puntaje_seo            INT│
│    │ fotos_calidad          INT│
│    │ atributos_completos    INT│
│    │ visitas                INT│
│    │ conversion          DEC(5,2)│
└─────────────────────────────────┘

┌─────────────────────────────────┐
│     metricas_reputacion         │
├─────────────────────────────────┤
│ PK │ id                     INT│
│    │ fecha                 DATE│
│    │ insignia               VC│
│    │ reclamos               INT│
│    │ mediaciones            INT│
│    │ devoluciones           INT│
│    │ logistica_puntaje      INT│
└─────────────────────────────────┘

┌─────────────────────────────────┐
│       metricas_costos           │
├─────────────────────────────────┤
│ PK │ id_venta                INT│
│    │ monto_bruto       DEC(10,2)│
│    │ comision          DEC(10,2)│
│    │ cargo_envio       DEC(10,2)│
│    │ monto_neto        DEC(10,2)│
│    │ margen_ganancia   DEC(5,2) │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│       metricas_envios           │
├─────────────────────────────────┤
│ PK │ id_venta                INT│
│    │ fecha_despacho         DATE│
│    │ fecha_entrega          DATE│
│    │ demora_dias            INT│
│    │ expuesto_penalizacion  BOOL│
└─────────────────────────────────┘

┌─────────────────────────────────┐
│       metricas_stock            │
├─────────────────────────────────┤
│ PK │ sku                     VC│
│    │ stock_total            INT│
│    │ stock_antiguo_dias     INT│
│    │ sobrestock_cargos DEC(10,2)│
│    │ calidad_puntaje        INT│
└─────────────────────────────────┘

┌─────────────────────────────────┐
│        diagnosticos             │
├─────────────────────────────────┤
│ PK │ id_diagnostico          INT│
│    │ fecha                 DATE│
│    │ area                   VC│
│    │ problema              TXT│
│    │ severidad              VC│
│    │ solucion_sugerida     TXT│
└──────────┬──────────────────────┘
           │ 1
           │
           │ N
┌──────────▼──────────────────────┐
│       planes_accion             │
├─────────────────────────────────┤
│ PK │ id_accion               INT│
│ FK │ id_diagnostico          INT│
│    │ tarea                  TXT│
│    │ prioridad              INT│
│    │ completado            BOOL│
└─────────────────────────────────┘
```
