//
//  ViewController.swift
//  SORTbot
//
//  Created by Rosu Octavian on 13/03/17.
//  Copyright © 2017 SORTbot team. All rights reserved.
//

import UIKit

var userID: Int = 0 // the userID. Helps us to 

class ViewController: UIViewController, UITextFieldDelegate {

    @IBOutlet weak var usernameTextField: UITextField!
    @IBAction func loginAction(_ sender: UIButton) {
        let good_credentials = self.check_credentials()
        
        if (!good_credentials) {
            return
        } else {
            
            let next = self.storyboard?.instantiateViewController(withIdentifier: "TabBarView")
            self.present(next!, animated: true, completion: nil)
        }
    }
    @IBOutlet weak var passTextField: UITextField!
    
   
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        self.usernameTextField.delegate = self
        self.passTextField.delegate = self
        
        self.passTextField.isSecureTextEntry = true
        
        self.resetFields()
        
    }
    
    private func resetFields() {
        self.usernameTextField.text = ""
        self.passTextField.text = ""
    }
    
    override func viewDidAppear(_ animated: Bool) {
        self.resetFields()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    private func check_credentials() -> Bool{
        //TODO: make a request to the server in order to get the feedback
        
        if (self.usernameTextField.text != "admin" || self.passTextField.text != "pass") {
            self.showMessage(message: "Wrong username or password")
            return false
        }
        
        return true
    }
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        self.view.endEditing(true)
        return false
    }
    
    private func showMessage(message msg: String, title: String = "ERROR", buttonMessage: String = "ok") {
        let alert = UIAlertView()
        alert.title = title
        alert.message = msg
        alert.addButton(withTitle: buttonMessage)
        alert.show()
    }

}

