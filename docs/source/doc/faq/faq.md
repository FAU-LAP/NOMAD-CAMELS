# Frequently Asked Questions - FAQs

Here you can find help for the most frequently asked questions regarding all aspects of CAMELS. Click on the answers to go to more in-depth descriptions and explanations.

<!-- Search Input -->
<input type="text" id="searchInput" placeholder="Search FAQs..." onkeyup="filterFAQs()" />

<!-- FAQ Container -->
<div class="box-container" id="faqContainer">
    <!-- FAQ Item -->
    <a href="../installation/installation.html" class="box">
    <span class="box-title">What do I need to install CAMELS?</span>
    <p class="box-content">All you need to install CAMELS is a Python +3.11 environment. Then run <code>pip install nomad-camels</code>.</p>
    </a>
    <a href="../api/api_landing.html" class="box">
    <span class="box-title">How do I control CAMELS from a different program?</span>
    <p class="box-content">If you want to control your CAMELS software with another program you can use CAMELS' API. This is especially useful if you have existing scripts but now want to control specific (new) aspects with CAMELS while still using the script you already have.</p>
    <span class="more-link" onclick="toggleContent(event, this)">More</span>
    </a>
    <a href="troubleshooting.html" class="box">
    <span class="box-title">My instrument is not recognized</span>
    <p class="box-content">If CAMELS does not recognize your instrument, some libraries might be missing.</p>
    </a>
    <a href="" class="box">
    <span class="box-title">The plots show no data</span>
    <p class="box-content">This may be due to an incorrect installation of a dependent package. Try updating:<code>pip install pyside6<span>&#60;</span>6.9 --upgrade</code>.</p>
    </a>
    <a href="troubleshooting.html" class="box">
    <span class="box-title">Any other problem</span>
    <p class="box-content">Click here to see general troubleshooting help.</p>
    </a>
</div>


```{eval-rst}
.. toctree::
   :hidden:
   :maxdepth: 2

   Troubleshooting <troubleshooting.md>
```
