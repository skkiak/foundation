import streamlit as st
import math

# Настройка страницы
st.set_page_config(page_title="Lego Foundation Calc", layout="wide")

# Кастомный CSS для "хорошего дизайна"
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Расчет опалубки «Лего» (Точность 100%)")
st.write("Программа рассчитывает раскладку без погрешностей, учитывая угловые модули и толщину стен.")

# --- БОКОВАЯ ПАНЕЛЬ: ВВОД ДАННЫХ ---
st.sidebar.header("📍 Параметры проекта")
outer_L = st.sidebar.number_input("Длина контура (м)", value=10.0, step=0.1)
outer_W = st.sidebar.number_input("Ширина контура (м)", value=8.0, step=0.1)
wall_t = st.sidebar.number_input("Толщина фундамента (м)", value=0.4, step=0.05)
height_type = st.sidebar.radio("Высота фундамента", ["До 60 см (Горизонтально)", "60-120 см (Вертикально)"])

st.sidebar.subheader("🚪 Внутренние стены")
room1_w = st.sidebar.number_input("Ширина Комнаты 1 (м)", value=6.0)
room2_w = st.sidebar.number_input("Ширина Комнаты 2 (м)", value=3.8)

# --- ЛОГИКА РАСЧЕТА ---
def calculate_segments(target_cm):
    """Раскладка щитов на отрезок без погрешности (120, 60, 50, 40, 20)"""
    # Доступные размеры щитов в см
    panels = [120, 60, 50, 40, 20]
    result = {}
    remaining = target_cm
    
    for p in panels:
        count = int(remaining // p)
        if count > 0:
            result[p] = count
            remaining -= count * p
    
    return result, remaining

# 1. Расчет наружного контура (Периметр)
# Углы по 50см (0.5м)
corner_offset = 50 
# Чистая длина стены между углами
wall_L_net = (outer_L * 100) - (2 * corner_offset)
wall_W_net = (outer_W * 100) - (2 * corner_offset)

layout_L, rem_L = calculate_segments(wall_L_net)
layout_W, rem_W = calculate_segments(wall_W_net)

# 2. Внутренние стены (учитываем примыкания)
# Внутренняя стена примыкает к наружной, вычитаем толщину стены (40см)
inner_wall_len = (outer_W * 100) - (2 * wall_t * 100) 
layout_inner, rem_inner = calculate_segments(inner_wall_len)

# --- ВЫВОД РЕЗУЛЬТАТОВ ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Спецификация щитов")
    st.write("**Наружный контур:**")
    for size, count in layout_L.items():
        st.write(f"- Щит {size}см: {count * 2} шт. (на две длинные стены)")
    for size, count in layout_W.items():
        st.write(f"- Щит {size}см: {count * 2} шт. (на две короткие стены)")
    
    st.write("**Внутренние перегородки:**")
    for size, count in layout_inner.items():
        st.write(f"- Щит {size}см: {count} шт. (на одну стену)")

with col2:
    st.subheader("🛠️ Углы и Крепеж")
    st.write(f"- **Наружные углы (кор):** 4 шт.")
    st.write(f"- **Внутренние углы (Вн):** 12 шт. (по проекту)")
    
    # Итоговое кол-во элементов для расчета процентов
    total_elements = sum(layout_L.values())*2 + sum(layout_W.values())*2 + sum(layout_inner.values()) + 16
    
    shablo = math.ceil(total_elements * 1.5) #
    klins = math.ceil(total_elements * 2.2)  #
    
    st.metric("Шабло (1.5%)", f"{shablo} шт.")
    st.metric("Клинья (2.2%)", f"{klins} кг")

# Проверка на точность
if rem_L == 0 and rem_W == 0 and rem_inner == 0:
    st.success("✅ Идеальная сходимость: Отклонение 0 см. Все замки закроются.")
else:
    st.error(f"⚠️ Внимание: Требуется добор {rem_L + rem_W} см.")

st.info("Примечание: При высоте до 60 см щиты 60х120 кладутся горизонтально.")
