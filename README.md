<div class="application-main " data-commit-hovercards-enabled="" data-discussion-hovercards-enabled="" data-issue-and-pr-hovercards-enabled="">
<div class=""><main id="js-repo-pjax-container" data-pjax-container="">
<div class="container-xl clearfix new-discussion-timeline px-3 px-md-4 px-lg-5">
<div id="repo-content-pjax-container" class="repository-content ">
<div>
<div class="Box mt-3 position-relative
    " data-target="readme-toc.content">
<div id="readme" class="Box-body readme blob js-code-block-container p-5 p-xl-6 gist-border-0">
<article class="markdown-body entry-content container-lg">
<p align="center">&nbsp;</p>
<h3 align="center">Cisco Nexus Data Broker Northbound Programming Interface</h3>
<p style="text-align: center;"><strong>High Level API to control and manage NDB</strong></p>
<details open="open">
<summary>Table of Contents</summary>
<ol>
<li><a href="#about-the-project">About The Project</a>
<ul>
<li><a href="#built-with">Built With</a></li>
</ul>
</li>
<li><a href="#getting-started">Getting Started</a>
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
<h2><a id="user-content-about-the-project" class="anchor" href="#about-the-project" aria-hidden="true"></a>About The Project</h2>
<p>Cisco Nexus Data Broker is Cisco&rsquo;s proprietary software defined packet broker, which has a simple and intuitive web-based UI to manage aggregation, filtering, forwarding, and replicating rules programmed on Cisco Nexus Datacenter switches mainly Nexus 3000 , 3500 and 9000. NBD exposes Northbound REST APIs to automate and adapt NDB configurations and rules dynamically. NDB has Southbound API implementation to either use protocols such as Openflow or NX-API over HTTP.</p>
<p>&nbsp;</p>
This API set mainly focuses on designing and coding high level client-side APIs using Python scripting language that can be used as a programming interface by 3<sup>rd</sup> party tools/applications. These API&rsquo;s will internally access REST full APIs to control and manage NDB controller&rsquo;s configurations and connections (filters and rules).&nbsp; Project aims at reducing the end user effort with simple, effective and minimal usage of high-level API by hiding more complex code internally.&nbsp; API development and coding will be adhering to Open-API standards (Open Api specification 3.0 &ndash; OAS3). <br />
<h3><a id="user-content-built-with" class="anchor" href="#built-with" aria-hidden="true"></a>Built With</h3>
<p>This project is mainly built over Python 3.x leveraging object oriented approach for more modularity and code reuse. High-Level APIs are purely Python based and underlying calls are REST-APIs to NDB controller. REST APIs swagger spec is part of this commit. </p>
<ul>
<li>Python 3.x</li>
<li>REST API</li>
</ul>
<h2><a id="user-content-getting-started" class="anchor" href="#getting-started" aria-hidden="true"></a>Getting Started</h2>
<p>To run this project you need a topology with Cisco nexus data broker, Cisco nexus Datacenter switches and a python environment. All the devices are interconnected and is reachable over IP network. More details below.</p>
<h3><a id="user-content-prerequisites" class="anchor" href="#prerequisites" aria-hidden="true"></a>Prerequisites</h3>
<p>Step-1</p>
<p>====</p>
<p>Install Cisco Nexus Data Broker which is a Java based application that can be installed on a linux server of your choice. Java version should be 8 or greater. In a working environment Ubunt 16.04 is used with openjdk-8</p>
<p>&nbsp;apt-get -y install openjdk-8-jdk</p>
<p>Step-2<br />====<br />Download Cisco Nexus Data Broker 3.9.0 from Cisco.com downloads to the linux server<br />Start the NDB server by going to xnc folder and executing ./runxnc.sh</p>
<p>From there on you should be able to access NDB from browser using https://&lt;IP-ADDRESS&gt;:8443/ (username: admin / password: admin)</p>
<p>Step-3<br />====<br />Use the swagger api spec file (NDB-swagger-spec-3.9.0.spec) committed to this project to create the swagger-api set. To auto generate the complete REST-API code in python, you can use Swagger code-generator. To install a docker container having swagger generator, please follow the below link</p>
<p>https://hub.docker.com/r/swaggerapi/swagger-generator/</p>
<p>Once the swagger generator docker is up, you can access it over web browser where docker is running. Import the swagger spec in the swagger generator and choose python as the preferred language and generate the complete Python based REST-API wrappers</p>
<h3><a id="user-content-installation" class="anchor" href="#installation" aria-hidden="true"></a>Installation</h3>
<ol>
<li>Download all the High-Level APIs from this project either into a different linux server or you can use the same NDB server itself. <br />In the same folder where you downloaded the project APIs, copy the swagger-api folder to the project folder
<div class="highlight highlight-source-js position-relative" data-snippet-clipboard-copy-content="const API_KEY = 'ENTER YOUR API';
">
<pre>&nbsp;</pre>
</div>
</li>
</ol>
<h2><a id="user-content-usage" class="anchor" href="#usage" aria-hidden="true"></a>Usage</h2>
<p>python orchestrator.py</p>
<p>Please refere orchestrator.py to know what inputs needs to be given to the script as mandatory. It's clearly documented.</p>
<h2><a id="user-content-roadmap" class="anchor" href="#roadmap" aria-hidden="true"></a>Roadmap</h2>
<p>- Develop the remaining modules and fill the gaps in automating NDB.<br />- Focus on specific features like ERSPAN/MPLS/QinQ stripping/ePBR Service chaining automation which is Cisco proprietory<br />- Test the API set end to end. <br />- Have proper catch statements to report and failures due to traceback <br />- Logging mechanisms to be implemented<br />- Look into Scalability and performance which are the key points<br />- Use Multi-threading wherever applicable.<br />- Comparison study with other similar work</p>
<h2><a id="user-content-license" class="anchor" href="#license" aria-hidden="true"></a>License</h2>
<p>Distributed under the GPL License. See <code>LICENSE</code> for more information.</p>
<h2><a id="user-content-contact" class="anchor" href="#contact" aria-hidden="true"></a>Contact</h2>
<p>Vinu Chandran - chandran.vinu@gmail.com</p>
<p>Project Link: <a href="https://github.com/your_username/repo_name">https://github.com/vinoos78/cisco-ndb</a></p>
</article>
</div>
</div>
</div>
</div>
</div>
</main></div>
</div>
<div class="zeroclipboard-container position-absolute right-0 top-0">&nbsp;</div>
