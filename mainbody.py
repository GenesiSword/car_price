"""
GUI structure.
"""

import wx
import webminer
import cardata


class Shape3(wx.Frame):
    """
    Class where price of the car with data entered by user can be calculate.

    Methods:
        init_ui_3()
        get_year()
        get_mileage()
        get_capacity()
        get_fuel()
        pass_price()
        on_close_3()
    """

    def __init__(self, *args, **kwargs, ):
        super(Shape3, self).__init__(*args, **kwargs)
        self.init_ui_3()

    def init_ui_3(self):
        """
        Window where user can prepare model for calculating car price,
        enter data and calculate car price.

        Widgets by which user can interact with program:

        button31 -> Prepare model.
        button32 -> Calculate.
        button33 -> Exit.
        button34 -> Approve year.
        button35 -> Approve mileage.
        button36 -> Approve capacity.
        fuel_cb31 -> Choose fuel.

        self.year_txt -> Field of input for year of production.
        self.mileage_txt -> Field of input for mileage
        self.capacity_txt -> Field of input for capacity.

        """
        pnl3 = wx.Panel(self)

        # Description

        txt31 = """
        You can calculate here your car price based on downloaded data.
        To calculate price you have to perform following instructions:
        1) Click button 'Prepare model' to prepare algorithm which will make calculations for you. 
        2) Enter required data and click button 'Calculate'.
        """
        vbox31 = wx.BoxSizer(wx.VERTICAL)
        font31 = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        st31 = wx.StaticText(pnl3, label=txt31, style=wx.ALIGN_CENTER)
        st31.SetFont(font31)
        vbox31.Add(st31, flag=wx.CENTER)
        pnl3.SetSizer(vbox31)

        wx.StaticLine(pnl3, pos=(25, 185), size=(750, 2))

        # Fields for input.

        self.price_txt = wx.TextCtrl(pnl3,
                                     value="Price: Not predicted yet",
                                     pos=(300, 460),
                                     size=(200, 30),
                                     style=wx.TE_READONLY)

        brand_txt = wx.TextCtrl(pnl3,
                                value=webminer.Mining.brand_name,
                                pos=(50, 200),
                                size=(200, 30),
                                style=wx.TE_READONLY)

        vehicle_txt = wx.TextCtrl(pnl3,
                                  value=webminer.Mining.vehicle_name,
                                  pos=(50, 240),
                                  size=(200, 30),
                                  style=wx.TE_READONLY)

        self.year_txt = wx.TextCtrl(pnl3,
                                    value="Year of production",
                                    pos=(50, 280),
                                    size=(200, 30))

        self.mileage_txt = wx.TextCtrl(pnl3,
                                       value="Mileage [km]",
                                       pos=(50, 320),
                                       size=(200, 30))

        self.capacity_txt = wx.TextCtrl(pnl3,
                                        value="Capacity [cm3]",
                                        pos=(50, 360),
                                        size=(200, 30))

        fuel_option = ['Benzyna', 'Benzyna+LPG', 'Diesel']

        fuel_cb31 = wx.ComboBox(pnl3,
                                pos=(50, 400),
                                size=(200, 30),
                                choices=fuel_option,
                                style=wx.CB_READONLY)
        fuel_cb31.Bind(wx.EVT_COMBOBOX, self.get_fuel)

        # Static Texts

        self.static31 = wx.StaticText(pnl3,
                                      label='Value not approved',
                                      pos=(430, 285),
                                      size=(200, 30))

        self.static32 = wx.StaticText(pnl3,
                                      label='Value not approved',
                                      pos=(430, 325),
                                      size=(200, 30))

        self.static33 = wx.StaticText(pnl3,
                                      label='Value not approved',
                                      pos=(430, 365),
                                      size=(200, 30))

        self.static34 = wx.StaticText(pnl3,
                                      label='Value not approved',
                                      pos=(430, 405),
                                      size=(200, 30))

        # Buttons.

        button31 = wx.Button(pnl3,
                             label='Prepare model',
                             pos=(350, 120),
                             size=(100, 50))
        button31.Bind(wx.EVT_BUTTON, cardata.Collector.prepare_algorithm)

        button32 = wx.Button(pnl3,
                             label='Calculate',
                             pos=(50, 450),
                             size=(100, 50))
        button32.Bind(wx.EVT_BUTTON, self.pass_price)

        button33 = wx.Button(pnl3,
                             label='Exit',
                             pos=(700, 440),
                             size=(70, 70))
        button33.Bind(wx.EVT_BUTTON, self.on_close_3)

        button34 = wx.Button(pnl3,
                             label='Year --> Approve',
                             pos=(270, 280),
                             size=(140, 30))
        button34.Bind(wx.EVT_BUTTON, self.get_year)

        button35 = wx.Button(pnl3,
                             label='Mileage --> Approve',
                             pos=(270, 320),
                             size=(140, 30))
        button35.Bind(wx.EVT_BUTTON, self.get_mileage)

        button36 = wx.Button(pnl3,
                             label='Capacity --> Approve',
                             pos=(270, 360),
                             size=(140, 30))
        button36.Bind(wx.EVT_BUTTON, self.get_capacity)

        # Window settings.

        self.SetSize((800, 560))
        self.SetTitle('Data settings')
        self.Centre()

    def get_year(self, event):
        """
        Get value from self.year_txt.
        """
        cardata.Calculate.year_calc = self.year_txt.GetValue()
        self.static31.SetLabel(cardata.Calculate.year_calc)

    def get_mileage(self, event):
        """
        Get value from self.mileage_txt.
        """
        cardata.Calculate.mileage_calc = self.mileage_txt.GetValue()
        self.static32.SetLabel(cardata.Calculate.mileage_calc)

    def get_capacity(self, event):
        """
        Get value from self.capacity_txt.
        """
        cardata.Calculate.capacity_calc = self.capacity_txt.GetValue()
        self.static33.SetLabel(cardata.Calculate.capacity_calc)

    def get_fuel(self, event):
        """
        Get value from fuel_cb31.
        """
        fuel_value = event.GetString()
        self.static34.SetLabel(fuel_value)
        cardata.Calculate.fuel_calc = fuel_value

    def pass_price(self, event):
        """
        Prepare model and calculate price of the car with given setting.
        """
        cardata.execute_prediction(self)
        price_string = 'Predicted price is: ' + str(cardata.Calculate.predicted_price)
        self.price_txt.SetValue(price_string)

    def on_close_3(self, event):
        """
        Close the window.
        """
        self.Close(True)


class Shape2(wx.Frame):
    """
    Class where user can enter brand and vehicle name of a car and start
    downloading data for this car.

    Methods:
        init_ui_2()
        get_brand()
        get_vehicle()
        on_close_2()
    """
    def __init__(self, *args, **kwargs,):
        super(Shape2, self).__init__(*args, **kwargs)
        self.init_ui_2()

    def init_ui_2(self):
        """
        Window with space where user can enter brand and vehicle name
        of a car and start downloading data for this car.

        Widgets by which user can interact with program:
        
        button21 -> Approve brand name.
        button22 -> Approve vehicle name.
        button23 -> Download data.
        button24 -> Exit.

        self.brand_name_txt -> Field of input for brand name.
        self.vehicle_name_txt -> Field of input for vehicle name.
        """
        pnl2 = wx.Panel(self)

        # Description
        
        txt21 = '''
        Enter brand and vehicle name of car which you want to collect data about.
        You approve your choice with a correct button. 
        Remember to choose the right names.'''
        vbox21 = wx.BoxSizer(wx.VERTICAL)
        font21 = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        st21 = wx.StaticText(pnl2, label=txt21, style=wx.ALIGN_CENTER)
        st21.SetFont(font21)
        vbox21.Add(st21, flag=wx.CENTER)
        pnl2.SetSizer(vbox21)
        
        # Fields for input.
        
        self.brand_name_txt = wx.TextCtrl(pnl2,
                                          value="Enter here brand name (eg. Audi)",
                                          pos=(300, 130),
                                          size=(200, 30))

        self.vehicle_name_txt = wx.TextCtrl(pnl2,
                                            value="Enter here vehicle name (eg. A3)",
                                            pos=(300, 250),
                                            size=(200, 30))
        
        # Buttons.
        
        button21 = wx.Button(pnl2,
                             label='Approve brand name',
                             pos=(300, 180),
                             size=(200, 50))
        button21.Bind(wx.EVT_BUTTON, self.get_brand)

        button22 = wx.Button(pnl2, label='Approve vehicle name',
                             pos=(300, 300),
                             size=(200, 50))
        button22.Bind(wx.EVT_BUTTON, self.get_vehicle)

        button23 = wx.Button(pnl2, label='Download data',
                             pos=(275, 420),
                             size=(250, 50))
        button23.Bind(wx.EVT_BUTTON, webminer.execute)

        button24 = wx.Button(pnl2, label='Exit',
                             pos=(700, 440),
                             size=(70, 70))
        button24.Bind(wx.EVT_BUTTON, self.on_close_2)
        
        # Window settings.

        self.SetSize((800, 560))
        self.SetTitle('Data settings')
        self.Centre()

    def get_brand(self, event):
        """
        Get value from self.brand_name_txt.
        """
        webminer.Mining.brand_name = self.brand_name_txt.GetValue()

    def get_vehicle(self, event):
        """
        Get value from self.vehicle_name_txt.
        """
        webminer.Mining.vehicle_name = self.vehicle_name_txt.GetValue()

    def on_close_2(self, event):
        """
        Close the window.
        """
        self.Close(True)


class Shape(wx.Frame):
    """
    Class with main GUI window.

    Methods:
        init_ui()
        on_close()
        on_save_as()
    """
    def __init__(self, *args, **kwargs):
        super(Shape, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        """
        Main window for managing program.

        button1 -> Download data.
        button2 -> Export data to .csv
        button3 -> Price calculator
        button4 -> Close
        """

        pnl = wx.Panel(self)

        # Image and its description.

        image_file = 'coupe.jpg'
        jpg1 = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        wx.StaticBitmap(pnl,
                        -1,
                        jpg1,
                        (130, 50),
                        (jpg1.GetWidth(), jpg1.GetHeight()))

        st11 = wx.StaticText(pnl,
                             label='Photo by Jesse Collins on Unsplash',
                             pos=(320, 490),
                             size=(200, 30))

        # Buttons.

        button1 = wx.Button(pnl,
                            label='Download data',
                            pos=(20, 40),
                            size=(100, 90))
        button1.Bind(wx.EVT_BUTTON, shape2ex)

        button2 = wx.Button(pnl,
                            label='Export data to .csv',
                            pos=(20, 160),
                            size=(100, 90))
        button2.Bind(wx.EVT_BUTTON, self.on_save_as)

        button3 = wx.Button(pnl,
                            label='Price calculator',
                            pos=(20, 280),
                            size=(100, 90))
        button3.Bind(wx.EVT_BUTTON, shape3ex)

        button4 = wx.Button(pnl,
                            label='Close',
                            pos=(20, 400),
                            size=(100, 90))
        button4.Bind(wx.EVT_BUTTON, self.on_close)

        # Window settings.

        self.SetSize((800, 560))
        self.SetTitle('Car Pricer')
        self.Centre()

    def on_close(self, event):
        """
        Close the window.
        """
        self.Close(True)

    def on_save_as(self, event):
        """
        Save data downloaded from website.
        """
        with wx.FileDialog(self, "Save XYZ file",
                           wildcard="CSV files (*.csv)|*.csv",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:

            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = file_dialog.GetPath()
            cardata.export_to_csv(self, path=pathname)


def main():
    """
    Mainloop with GUI structure.
    """
    app = wx.App()
    frame = Shape(None, title='Car prices')
    frame.Show()
    app.MainLoop()


def shape2ex(self):
    """
    Function asking about website address and displaying GUI window
    defined in Shape2 class.
    It is executed with button1 in init_ui_2(self).
    """

    dlg11 = wx.TextEntryDialog(None,
                               ('Enter website address in a '
                                'format, e.g.: www.google.com'),
                               'Website')

    if dlg11.ShowModal() == wx.ID_OK:
        webminer.Mining.source = dlg11.GetValue()
        frame2 = Shape2(None, title='Car prices')
        frame2.Show()

    dlg11.Destroy()


def shape3ex(self):
    """
    Function displaying GUI window defined in Shape3 class.
    It is executed with button1 in init_ui_3(self).
    """
    frame3 = Shape3(None, title='Price calculator')
    frame3.Show()


if __name__ == '__main__':
    main()
