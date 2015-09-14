# Issue analyze failed w/ 404

## problem description
Running:

    gradle sonarqube --stacktrace

Generates exception like:

    Caused by: org.sonar.api.utils.HttpDownloader$HttpException: Fail to
    download [http://192.168.33.40:9000/deploy/plugins/index.txt]. Response
    code: 404
        at
    org.sonar.api.utils.HttpDownloader$BaseHttpDownloader$HttpInputSupplier.getInput(HttpDownloader.java:305)
        at
    org.sonar.api.utils.HttpDownloader$BaseHttpDownloader$HttpInputSupplier.getInput(HttpDownloader.java:255)
        at
    org.sonar.batch.bootstrap.ServerClient.request(ServerClient.java:105)
        ... 76 more


## root cause analysis
SonarQube 5.1.2 use embedded tomcat 8 and the way to instruct tomcat to
follow symlink changes. Previously, the "allowLinking" is the attribute
of "Contex" element, now it belongs to "Resources" element:

    <!-- Tomcat 7: -->
    <Context allowLinking="true" />

    <!-- Tomcat 8: -->
    <Context>
      <Resources allowLinking="true" />
    </Context>

## The fix
Update the context.xml w/ following content:

    <?xml version="1.0" encoding="UTF-8"?>
    <Context path="/">
      <Resources allowLinking="true" />
    </Context>
