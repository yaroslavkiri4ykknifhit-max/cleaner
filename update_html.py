import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update header menu
header_menu_target = """<a href="#services" class="text-sm font-semibold text-gray-800 hover:text-accent transition-colors">УСЛУГИ</a>
                <a href="#benefits" class="text-sm font-semibold text-gray-800 hover:text-accent transition-colors">ПРЕИМУЩЕСТВА</a>"""
header_menu_replacement = """<a href="#services" class="text-sm font-semibold text-gray-800 hover:text-accent transition-colors">УСЛУГИ</a>
                <a href="#portfolio" class="text-sm font-semibold text-gray-800 hover:text-accent transition-colors">РАБОТЫ</a>
                <a href="#benefits" class="text-sm font-semibold text-gray-800 hover:text-accent transition-colors">ПРЕИМУЩЕСТВА</a>"""
content = content.replace(header_menu_target, header_menu_replacement)

# 2. Update footer menu
footer_menu_target = """<a href="#services" class="hover:text-white transition-colors">Услуги</a>
                    <a href="#prices" class="hover:text-white transition-colors">Цены</a>"""
footer_menu_replacement = """<a href="#services" class="hover:text-white transition-colors">Услуги</a>
                    <a href="#portfolio" class="hover:text-white transition-colors">Работы</a>
                    <a href="#prices" class="hover:text-white transition-colors">Цены</a>"""
content = content.replace(footer_menu_target, footer_menu_replacement)

# 3. Insert portfolio section
portfolio_section = """
    <!-- Portfolio (Before/After) -->
    <section id="portfolio" class="py-24 bg-white border-t border-gray-100">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-16">
                <h2 class="text-4xl md:text-6xl font-extrabold text-gray-900 uppercase tracking-tight mb-4">Наши работы</h2>
                <p class="text-xl text-gray-600 font-medium">Результаты химчистки в формате «До и После»</p>
            </div>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">"""

for i in range(11):
    idx_before = 3928 + i*2
    idx_after = 3929 + i*2
    portfolio_section += f"""
                <!-- Pair {i+1} -->
                <div class="rounded-[32px] overflow-hidden shadow-lg flex flex-col sm:flex-row h-auto sm:h-[300px] border border-gray-100 bg-[#f8f9fa]">
                    <div class="relative w-full sm:w-1/2 h-[250px] sm:h-full">
                        <img src="images/IMG_{idx_before}.PNG" alt="До" class="w-full h-full object-cover">
                        <div class="absolute top-4 left-4 bg-gray-900/80 backdrop-blur-sm text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">До</div>
                    </div>
                    <div class="relative w-full sm:w-1/2 h-[250px] sm:h-full border-t sm:border-t-0 sm:border-l border-gray-200">
                        <img src="images/IMG_{idx_after}.PNG" alt="После" class="w-full h-full object-cover">
                        <div class="absolute top-4 right-4 bg-accent/90 backdrop-blur-sm text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">После</div>
                    </div>
                </div>"""

portfolio_section += """
            </div>
        </div>
    </section>

"""

services_end_target = """    </section>

    <!-- Benefits (Minimalist layout) -->"""
services_end_replacement = "    </section>\n" + portfolio_section + "    <!-- Benefits (Minimalist layout) -->"
content = content.replace(services_end_target, services_end_replacement)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updates applied successfully.")
