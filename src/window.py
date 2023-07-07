# window.py
#
# Copyright 2023 Francisco Jeferson dos Santos Freires
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import re
from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gio
from currencyconverter.components import CurrencySelector
from currencyconverter.api import Api, CurrenciesListModel
from currencyconverter.settings import Settings
from currencyconverter.define import APP_ID

@Gtk.Template(resource_path='/io/github/idevecore/CurrencyConverter/ui/window.ui')
class CurrencyconverterWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CurrencyconverterWindow'

    # lang_list = Gtk.Template.Child()
    src_currency_selector: CurrencySelector = Gtk.Template.Child()
    dest_currency_selector: CurrencySelector = Gtk.Template.Child()
    src_currencies = []
    dest_currencies = []
    # search = Gtk.Template.Child()
    # provider = {
    #     'trans': None,
    #     'tts': None
    # }


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.src_currency_model = CurrenciesListModel(self._currency_names_func)
        self.dest_currency_model = CurrenciesListModel(self._currency_names_func)
        self.src_currency_selector.bind_models(self.src_currency_model)
        self.dest_currency_selector.bind_models(self.dest_currency_model)
        self.src_currency_model.set_langs(Api().codes)
        self.dest_currency_model.set_langs(Api().codes)
        self.connect('unrealize', self.save_settings)
        self.src_currencies = self.src_currency_model
        self.load_settings(APP_ID)
        if self.src_currencies is not None:
            self.src_currency_selector.set_selected(self.src_currencies)
            self.dest_currency_selector.set_selected(self.dest_currencies)

    def load_settings(self, id):
        self.settings = Gio.Settings.new(id);
        self.src_currencies = self.settings.get_string('src-currencies')
        self.dest_currencies = self.settings.get_string('dest-currencies')

    def _currency_names_func(self, code):
        return Api().codes[code]

    def save_settings(self, *args, **kwargs):
        self.settings.set_string('src-currencies', self.src_currencies)
        self.settings.set_string('dest-currencies', self.dest_currencies)

    @Gtk.Template.Callback()
    def _on_src_currency_changed(self, _obj, _param):
        code = self.src_currency_selector.selected
        self.src_currencies = code
        print(code)
        
    @Gtk.Template.Callback()
    def _on_dest_currency_changed(self, _obj, _param):
        code = self.dest_currency_selector.selected
        self.dest_currencies = code
        print(code)
