<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** fohs-score-tracker, service, twitter_handle, email, service, Backend for ScoreTracker.
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]




<!-- PROJECT LOGO -->
<!-- <br />
<p align="center">
  <a href="https://github.com/fohs-score-tracker/service">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> --> 

  <h3 align="center">Service</h3>

  <p align="center">
    Backend for ScoreTracker.
    <br />
    <a href="https://fohs-score-tracker.herokuapp.com"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <!-- <a href="https://fohs-score-tracker.herokuapp.com">View Demo</a> --> 
    ·
    <a href="https://github.com/fohs-score-tracker/service/issues">Report Bug</a>
    ·
    <a href="https://github.com/fohs-score-tracker/service/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With FastAPI</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!--[![Product Name Screen Shot][product-screenshot]](https://example.com) -->
  Back end API for ScoreTracker app.


<!-- Here's a blank template to get started:
**To avoid retyping too much info. Do a search and replace with your text editor for the following:**
`fohs-score-tracker`, `service`, `twitter_handle`, `email`, `service`, `Backend for ScoreTracker.` -->


### Built With

* [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
<!--* []() 
* []()-->



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

<!-- ### Prerequisites

This is an example of how to list things you need to use the software and how to install them.*  npm
  ```sh
  npm install npm@latest -g
  ``` -->

### Installation

1. Clone the repo
    ```
    git clone https://github.com/fohs-score-tracker/service.git
    ```

2. Change directory to service
    ```
    cd service
    ```

3. Install Python dependencies
    ```
    pip install -r requirements.txt
    ```
4. Environment variables are used for configuration (which can also be set in `.env`)

    Example config file: 

    ```sh
    REDIS_URL="redis://user:password@server/db"
    ```

    ℹ The database provided by the `REDIS_URL` variable is **not** used for testing.


<!-- USAGE EXAMPLES -->
## Usage
  ``` 
  uvicorn scoretracker:app
  ```  


<!--_For more examples, please refer to the [Documentation](https://example.com)_ -->



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/fohs-score-tracker/service/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `https://mit-license.org/` for more information.



<!-- CONTACT -->
## Contact

<!-- Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email -->

Project Link: [https://github.com/fohs-score-tracker/service](https://github.com/fohs-score-tracker/service)



<!-- ACKNOWLEDGEMENTS -->
##  Acknowledgements / Thanks
* 👤 **DaShaun Carter**
     - Github: [@dashaun](https://github.com/dashaun)
     - Twitter : [@dashaun](https://twitter.com/dashaun/)



 * 👤 **Phillip Hodges**
     - Github: [@phodges7727](https://github.com/phodges7727)







<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/fohs-score-tracker/service.svg?style=for-the-badge
[contributors-url]: https://github.com/fohs-score-tracker/service/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/fohs-score-tracker/service.svg?style=for-the-badge
[forks-url]: https://github.com/fohs-score-tracker/service/network/members
[stars-shield]: https://img.shields.io/github/stars/fohs-score-tracker/service.svg?style=for-the-badge
[stars-url]: https://github.com/fohs-score-tracker/service/stargazers
[issues-shield]: https://img.shields.io/github/issues/fohs-score-tracker/service.svg?style=for-the-badge
[issues-url]: https://github.com/fohs-score-tracker/service/issues
[license-shield]: https://img.shields.io/github/license/fohs-score-tracker/service.svg?style=for-the-badge
[license-url]: https://github.com/fohs-score-tracker/service/blob/master/LICENSE.txt

