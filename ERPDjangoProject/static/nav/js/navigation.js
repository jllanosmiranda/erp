
export function ActiveSubNav(sub_nav_id) {
    let subnav = document.getElementById(sub_nav_id);
    subnav.classList.add("active");
    console.log("ActiveSubNav");
    console.log(subnav);
}
