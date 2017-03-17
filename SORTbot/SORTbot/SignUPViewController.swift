//
//  SignUPViewController.swift
//  SORTbot
//
//  Created by Rosu Octavian on 13/03/17.
//  Copyright © 2017 SORTbot team. All rights reserved.
//

import UIKit

class SignUPViewController: UIViewController, UITextFieldDelegate {

    @IBOutlet weak var checkPassBox: UITextField!
    @IBOutlet weak var passBox: UITextField!
    @IBOutlet weak var userNameBox: UITextField!
    @IBOutlet weak var lastNameBox: UITextField!
    @IBOutlet weak var firstNameBox: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        

        let backButton = UIBarButtonItem(title: "", style: UIBarButtonItemStyle.plain, target: navigationController, action: nil)

        navigationItem.leftBarButtonItem = backButton
        
        self.checkPassBox.delegate = self
        self.passBox.delegate = self
        self.userNameBox.delegate = self
        self.lastNameBox.delegate = self
        self.firstNameBox.delegate = self
        
        self.checkPassBox.text = ""
        self.passBox.text = ""
        self.userNameBox.text = ""
        self.lastNameBox.text = ""
        self.firstNameBox.text = ""
    }
    
    @IBAction func cancelButtonAction(_ sender: UIButton) {
        let home = self.storyboard?.instantiateViewController(withIdentifier: "LoginViewController")
        self.present(home!, animated: true, completion: nil)
    }
    
    @IBAction func okButtonAction(_ sender: UIButton) {
        
        var all_good = self.check_fields()
        
        if (!all_good) {
            return
        }
        
        all_good = send_data()
        
        if (!all_good) {
            return
        } else {
            self.showMessage(message: "All done! ", title: "Yay!")
            // returning to root
            _ = navigationController?.popToRootViewController(animated: true)
        }
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        self.view.endEditing(true)
        return false
    }
    
    private func send_data() -> Bool {
        //TODO: (1) Implement the sender
        //      (2) Make the check if the user already exists in the database
        
        return true
    }
    
    private func check_fields() -> Bool{
        
        if ((self.passBox.text?.isEmpty)! || (self.checkPassBox.text?.isEmpty)! || (self.userNameBox.text?.isEmpty)! ||
            (self.lastNameBox.text?.isEmpty)! ||  (self.firstNameBox.text?.isEmpty)!) {
            self.showMessage(message: "No field can be empty!")
            return false
        }
        
        if self.passBox.text != self.checkPassBox.text {
            self.showMessage(message: "The passwords don't match")
            return false
        }
        
        return true
    }
    
    private func showMessage(message msg: String, title: String = "ERROR", buttonMessage: String = "ok") {
        let alert = UIAlertView()
        alert.title = title
        alert.message = msg
        alert.addButton(withTitle: buttonMessage)
        alert.show()
    }
    

}
