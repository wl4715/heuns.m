//
//  HomeViewController.swift
//  SORTbot
//
//  Created by Rosu Octavian on 14/03/17.
//  Copyright © 2017 SORTbot team. All rights reserved.
//

import UIKit

class HomeViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
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

    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
