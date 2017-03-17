//
//  AddViewController.swift
//  SORTbot
//
//  Created by Rosu Octavian on 14/03/17.
//  Copyright © 2017 SORTbot team. All rights reserved.
//

import UIKit
import Foundation

class AddViewController: UIViewController {

    @IBOutlet weak var MixedButton: UIButton!
    @IBOutlet weak var PaperButton: UIButton!
    @IBOutlet weak var CarboardButton: UIButton!
    @IBOutlet weak var PlasticButton: UIButton!
    
    var selectedButton: UIButton? = nil
    
    override func viewDidAppear(_ animated: Bool) {
        self.massEnable()
    }
    
    @IBAction func SignOutButton(_ sender: UIButton) {
        let alert = UIAlertController(title: "Sign out",
                                      message: "Are you sure?",
                                      preferredStyle: UIAlertControllerStyle.alert)
        
        // add the actions (buttons)
        alert.addAction(UIAlertAction(title: "Yes", style: UIAlertActionStyle.default, handler: { action in self.redirectHome() } ))
        alert.addAction(UIAlertAction(title: "No", style: UIAlertActionStyle.cancel, handler: nil))
        
        // show the alert
        self.present(alert, animated: true, completion: nil)
    }
    
    private func redirectHome() {
        let home = self.storyboard?.instantiateViewController(withIdentifier: "LoginViewController")
        self.present(home!, animated: true, completion: nil)
    }
    
    private func enableButton(_ btn: UIButton) {
        btn.isUserInteractionEnabled = true
        btn.setTitleColor(UIColor.white, for: .normal)
    }
    
    private func disableButton(_ btn:UIButton) {
        btn.isUserInteractionEnabled = false
        btn.setTitleColor(UIColor.black, for: .normal)
        
    }
    
    @IBAction func SelectorAction(_ sender: UIButton) {
        
        if selectedButton != nil {
            // this means something else was selected before this
            self.enableButton(selectedButton!)
        }
        
        selectedButton = sender
        self.disableButton(sender)
    }
    
    @IBAction func ConfirmAction(_ sender: UIButton) {
        if self.selectedButton == nil {
            // error
            self.showMessage(message: "You have to select a product before you confirm")
            return
        }
        
        let product = self.selectedButton!.titleLabel?.text
        let message = "You are about to confirm " + product! + ". Are you sure?"
        
        let alert = UIAlertController(title: "Confirm",
                                      message: message,
                                      preferredStyle: UIAlertControllerStyle.alert)
        
        // add the actions (buttons)
        alert.addAction(UIAlertAction(title: "Yes", style: UIAlertActionStyle.default, handler: { action in self.sendDataToServer() } ))
        alert.addAction(UIAlertAction(title: "No", style: UIAlertActionStyle.cancel, handler: nil))
        
        // show the alert
        self.present(alert, animated: true, completion: nil)
        
        
    }
    
    private func showMessage(message msg: String, title: String = "ERROR", buttonMessage: String = "ok") {
        let alert = UIAlertView()
        alert.title = title
        alert.message = msg
        alert.addButton(withTitle: buttonMessage)
        alert.show()
    }
    
    private func sendDataToServer() {
        //TODO: Send it to the server
        self.showMessage(message: "Database updated", title: "Done")
        self.massEnable()
    }
    
    private func massEnable() {
        self.enableButton(PlasticButton)
        self.enableButton(MixedButton)
        self.enableButton(CarboardButton)
        self.enableButton(PaperButton)
    }

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
