#Use this file to update files if needed.
#including this section makes some anti-virus systems think it is ransomware.
def update_settings_files(self):
        for file in next(os.walk(os.getcwd()))[2]:
            if file[-4:]=="SSS2":
                print("Opening {}".format(file))
                with open(file,'r') as infile:
                    self.settings_dict=json.load(infile)
                self.file_status_string.set("Opened "+file)
                self.settings_file_status_string.set(os.path.basename(file))

                self.settings_dict["SSS2 Product Code"] = "UNIVERSAL"
                
                self.settings_dict["SSS2 Interface Release Date"] = self.release_date
                self.settings_dict["SSS2 Interface Version"] = self.release_version

                ##Update all settings files with the default range
                self.settings_dict["HVAdjOut"]["Highest Voltage"] = 11.0
                self.settings_dict["HVAdjOut"]["Lowest Voltage"]= 1.9

                self.settings_dict["PWMs"]["PWM1"]["Lowest Frequency"]= 245
                self.settings_dict["PWMs"]["PWM2"]["Lowest Frequency"]= 245
                self.settings_dict["PWMs"]["PWM1"]["Frequency"]= 245
                self.settings_dict["PWMs"]["PWM2"]["Frequency"]= 245

                self.settings_dict["Potentiometers"]["Group B"]["Label"]="Potentiometers 9 though 16"
                self.settings_dict["Component ID"]= "SYNER*SSS2-R05*XXXX*UNIVERSAL"

                
                
                
                self.sss2_product_code['bg']='white'

                #self.saved_date_text.set(time.strftime("%A, %d %B %Y %H:%M:%S %Z", time.localtime()))
                
                self.settings_dict["SHA256 Digest"]=self.get_settings_hash()
                
                self.settings_dict["Original File SHA"]=self.settings_dict["SHA256 Digest"]
                

                 
                with open(file,'w') as outfile:
                    json.dump(self.settings_dict,outfile,indent=4,sort_keys=True)
                print("Saved {}".format(file))
                self.file_status_string.set("Saved "+file)
                self.settings_file_status_string.set(file)
