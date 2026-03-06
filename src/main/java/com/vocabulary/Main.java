package com.vocabulary;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class Main extends Application {

    private static UIController controller;

    @Override
    public void start(Stage primaryStage) throws Exception {
        javafx.scene.text.Font.loadFont(getClass().getResourceAsStream("/Nunito.ttf"), 14);

        FXMLLoader loader = new FXMLLoader(getClass().getResource("/app.fxml"));
        Parent root = loader.load();

        controller = loader.getController();

        Scene scene = new Scene(root, 820, 580);
        primaryStage.setTitle("Personal Vocabulary Tracker");
        primaryStage.getIcons().add(new javafx.scene.image.Image(getClass().getResourceAsStream("/icon.png")));
        primaryStage.setScene(scene);

        primaryStage.setOnCloseRequest(e -> {
            if (controller != null) {
                controller.shutdown();
            }
            Platform.exit();
            System.exit(0);
        });

        primaryStage.show();
        // Call AFTER show() so stage dimensions (including decorations) are known
        controller.setupZoom(scene);
    }

    public static void main(String[] args) {
        launch(args);
    }
}
